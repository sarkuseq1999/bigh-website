"""End-to-end test of the Support form's sending, without sending real email.

A local stand-in for Resend's API records what the site posts to it. Build and start the site with
the email settings pointing at it, then this script fills the real form in a browser (with a photo,
and once as a reaction report) and checks what reached the stand-in: two emails per message (the
message to the support inbox, the confirmation to the customer), the ticket on the page equal to
the ticket in both, reply-to set, the photo attached, the reaction marked urgent.

  1. python -X utf8 reference/launch/test_support_mail.py --serve      (stand-in on :3999)
  2. RESEND_API_KEY=test SUPPORT_EMAIL_FROM="BiGH <support@bighnow.com>" \\
     RESEND_API_BASE=http://localhost:3999 npm run build && npm start -- --port 3016
  3. python -X utf8 reference/launch/test_support_mail.py http://localhost:3016
"""

import json
import re
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

MOCK = "http://localhost:3999"
RECEIVED: list[dict] = []


class Stand(BaseHTTPRequestHandler):
    def do_POST(self):  # noqa: N802
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        body["_auth"] = self.headers.get("Authorization")
        RECEIVED.append(body)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"id": f"test-{len(RECEIVED)}"}).encode())

    def do_GET(self):  # noqa: N802 - the test reads what arrived
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(RECEIVED).encode())

    def do_DELETE(self):  # noqa: N802
        RECEIVED.clear()
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass


def serve():
    ThreadingHTTPServer(("localhost", 3999), Stand).serve_forever()


def received():
    with urllib.request.urlopen(MOCK) as r:
        return json.loads(r.read())


def clear():
    urllib.request.urlopen(urllib.request.Request(MOCK, method="DELETE"))


ok = fail = 0


def check(name, cond, detail=""):
    global ok, fail
    ok, fail = (ok + 1, fail) if cond else (ok, fail + 1)
    print("PASS" if cond else "FAIL", name, "" if cond else detail)


def run(base):
    from playwright.sync_api import sync_playwright

    photo = Path(__file__).resolve().parents[2] / "public/images/products/nuricell.png"
    with sync_playwright() as p:
        b = p.chromium.launch()
        page = b.new_page(viewport={"width": 1440, "height": 900})
        for topic, urgent in (("A health or science question", False), ("I had a reaction", True)):
            clear()
            # A new address each round: the same address again would only move to #write.
            page.goto(f"{base}/support?topic=science&round={int(urgent)}#write", wait_until="networkidle")
            page.wait_for_timeout(1500)
            text = page.locator("#write").inner_text()
            check(f"[{topic}] live form: no placeholder line", "aren’t sent yet" not in text and "ticket number comes by email" in text, text[:200])
            page.fill("#support-name", "Test Person")
            page.fill("#support-email", "customer@example.com")
            page.fill("#support-order", "A-1001")
            page.locator("label", has_text=topic).click()
            page.fill("#support-message", "Does acetyl-L-carnitine work with lipoic acid?")
            page.set_input_files("#support-photo", str(photo))
            page.click("form button[type=submit]")
            page.wait_for_selector("[data-ticket]", timeout=15000)
            ticket = page.locator("[data-ticket]").inner_text().strip()
            sent = page.locator("[data-sent]").inner_text()
            check(f"[{topic}] thank-you with a ticket", re.match(r"^BH-\d{4}-[A-Z2-9]{4}$", ticket) is not None, ticket)
            check(f"[{topic}] thank-you promises the email reply", "We’ll reply by email" in sent and "nothing was sent" not in sent, sent[:200])
            mails = received()
            check(f"[{topic}] two emails", len(mails) == 2, str(len(mails)))
            if len(mails) == 2:
                inbox, copy = mails
                check(f"[{topic}] to the support inbox", inbox["to"] == ["support@bighnow.com"], inbox["to"])
                check(f"[{topic}] reply-to the customer", inbox.get("reply_to") == "customer@example.com", inbox.get("reply_to"))
                check(f"[{topic}] ticket in both subjects", ticket in inbox["subject"] and ticket in copy["subject"], [inbox["subject"], copy["subject"]])
                check(f"[{topic}] urgent only for a reaction", inbox["subject"].startswith("URGENT") == urgent, inbox["subject"])
                check(f"[{topic}] message, order and topic in the body", "lipoic acid" in inbox["text"] and "A-1001" in inbox["text"] and topic in inbox["text"])
                att = inbox.get("attachments") or []
                check(f"[{topic}] photo attached", len(att) == 1 and att[0]["filename"] == "nuricell.png" and len(att[0]["content"]) > 1000, str([a.get("filename") for a in att]))
                check(f"[{topic}] confirmation to the customer", copy["to"] == ["customer@example.com"] and "1–2 business days" in copy["text"])
                check(f"[{topic}] sender and key", inbox["from"] == "BiGH <support@bighnow.com>" and inbox["_auth"] == "Bearer test")
        # A robot filling the hidden field: answered, nothing sent.
        clear()
        r = page.request.post(base + "/api/support", multipart={"name": "Bot", "email": "b@b.co", "topic": "An order", "message": "spam", "website": "http://spam"})
        check("honeypot: answered, nothing sent", r.ok and not received(), str(r.status))
        r = page.request.post(base + "/api/support", multipart={"name": "", "email": "nope", "topic": "x", "message": ""})
        check("invalid fields refused (422)", r.status == 422, str(r.status))
        b.close()


if __name__ == "__main__":
    if sys.argv[1:] == ["--serve"]:
        serve()
    else:
        run(sys.argv[1].rstrip("/"))
        print(f"\n{ok} passed, {fail} failed")
        sys.exit(1 if fail else 0)
