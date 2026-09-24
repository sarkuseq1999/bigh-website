"use client";

import { ArrowRight, LockKeyhole } from "lucide-react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./account-preview.module.css";

export function AccountPreview({ mode }: { mode: "login" | "signup" }) {
  const copy = useCopy();
  return (
    <div className={styles.account}>
      <p>
        {copy(
          mode === "login" ? "A little closer to good health." : "Your next chapter starts here.",
        )}
      </p>
      <div className={styles.notice}>
        <LockKeyhole size={18} aria-hidden="true" />
        <p>
          {copy(
            "Design preview only. Accounts are not connected yet, so these fields are disabled and no information is collected.",
          )}
        </p>
      </div>
      <fieldset disabled className={styles.fields}>
        <legend className={styles.srOnly}>{copy(mode === "login" ? "Log in" : "Sign up")}</legend>
        {mode === "signup" && (
          <label>
            {copy("Full name")}
            <input type="text" autoComplete="off" placeholder={copy("Your name")} />
          </label>
        )}
        <label>
          {copy("Email address")}
          <input type="email" autoComplete="off" placeholder="you@example.com" />
        </label>
        <label>
          {copy("Password")}
          <input type="password" autoComplete="off" placeholder="••••••••" />
        </label>
        <button type="button">
          {copy(mode === "login" ? "Log in" : "Create account")}
          <ArrowRight size={18} aria-hidden="true" />
        </button>
      </fieldset>
    </div>
  );
}
