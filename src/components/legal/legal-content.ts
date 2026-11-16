// The site's legal pages (November 16, 2026, for launch): BiGH's own Privacy Notice, Terms and
// Conditions and Return Policy, carried over from bighnow.com (each "Last update: 5/30/2016") with
// their wording kept. Changed only: spelling and typos ("misprized", "Complains"), a sentence the
// old Terms printed twice, a reference to "Mobile Alerts Terms of Use" that no longer exists, and
// the old role mailboxes (refund@, exchange@, complain@, info@) replaced by support@bighnow.com, the
// one address the new site gives (Mo confirmed the Support details on October 13, 2026). Have a
// lawyer review them before launch: they are 2016 documents (no "Do Not Track" or CCPA wording).
// English only, like the Support page.

export type LegalBlock =
  | { kind: "p"; text: string }
  | { kind: "list"; items: string[] }
  | { kind: "address"; lines: string[] };

export type LegalSection = { heading?: string; blocks: LegalBlock[] };

export type LegalDoc = {
  slug: "privacy" | "terms" | "returns";
  title: string;
  description: string;
  updated: string;
  sections: LegalSection[];
};

const p = (text: string): LegalBlock => ({ kind: "p", text });
const list = (...items: string[]): LegalBlock => ({ kind: "list", items });

const ADDRESS = ["BiGH Corporation", "2200 E Route 66, Suite 103", "Glendora, CA 91740", "USA"];

export const privacy: LegalDoc = {
  slug: "privacy",
  title: "Privacy Notice",
  description: "How BiGH collects, uses and protects your information.",
  updated: "November 16, 2026",
  sections: [
    {
      blocks: [
        p(
          "Keeping your information secure is a top priority for BiGH Corporation (“BiGH,” “we,” “us,” or “our”). This Privacy Notice outlines our views and practices and how they pertain to you as a visitor to www.bighnow.com (the “Site”). Please check back periodically, as these policies may change and your subsequent use of the Site will be deemed acceptance of such changes. However, our fundamental commitment to protecting your privacy will not change.",
        ),
      ],
    },
    {
      heading: "1. Collection of information",
      blocks: [
        p(
          "Information you volunteer. We only collect personally identifiable information you voluntarily provide while using our services, such as name, mailing address, email address, telephone number and payment card data. You may always choose not to provide us with information. However, we may not be able to provide you with the services you have requested. Visitors may access the Site without disclosing personally identifiable information.",
        ),
        p(
          "Information collected automatically. We do not automatically log personally identifiable information or link information automatically logged by other means with personally identifiable information about specific individuals. However, we may record non-personally identifiable information that becomes available to us through your use of the Site, including, without limitation, the number of visitors and frequency of visits to the Site. This information may include the websites that you access immediately before and after the Site, the Internet browser you use, and your IP address. If we use this information, it is only on an aggregate basis.",
        ),
        p(
          "Cookies and other similar technologies. Like most websites, we use cookies, or data files automatically stored on your computer, to enhance your visit to the Site by better understanding how visitors use the Site. In general, cookies do not contain any personally identifiable information unless you as a visitor knowingly supply the information. We use cookies in order to recognize you when you return to the Site and to provide you with a better user experience. We do not use cookies to store personally identifiable data or link non-personally identifiable information stored in cookies with personally identifiable information about specific individuals. We may allow third parties to use cookies or similar technologies on the Site but we do not control the use or contents of third-party cookies. Web browsers often permit you to erase cookies from your browser cache, block cookies, or receive notification when cookies are used.",
        ),
      ],
    },
    {
      heading: "2. Use of information",
      blocks: [
        p(
          "We use the information collected on the Site to provide you with the services you have requested, to serve you with content, and to enhance your overall experience while visiting the Site.",
        ),
      ],
    },
    {
      heading: "3. Sharing information with other parties",
      blocks: [
        p(
          "BiGH may use internal and external service providers to operate the Site and perform other work on our behalf in the course of providing you with services you have requested. These service providers may have access to your personally identifiable information, but are contractually bound to use your information only for the purpose of performing their duties.",
        ),
        p(
          "BiGH does not sell, trade or rent your personal information to any third parties for marketing purposes. We value your privacy and will not jeopardize our relationship with you by selling your information to solicitors without your prior consent.",
        ),
      ],
    },
    {
      heading: "4. Security of information",
      blocks: [
        p(
          "BiGH takes administrative, technical and physical measures to help ensure that your personally identifiable information remains accurate, timely and secure. However, no data transmission over the Internet, or through an electronic database, is guaranteed to be 100% secure. Although we strive to protect your information, we cannot guarantee or warrant its security.",
        ),
        p(
          "BiGH restricts access to personally identifiable information to our employees, contractors and agents who need to know that information in order to perform their jobs. They are obligated to respect the confidentiality of your personally identifiable information and may be disciplined or terminated for failing to meet these obligations.",
        ),
      ],
    },
    {
      heading: "5. Data safety, access and corrections",
      blocks: [
        p(
          "BiGH will keep personally identifiable information in active files or systems as long as necessary in order to fulfill the purposes for which it was collected. We will make reasonable efforts to ensure that the information is accurate and complete and will update or correct your information as needed when notified by you.",
        ),
      ],
    },
    {
      heading: "6. Children",
      blocks: [
        p(
          "The Site is a general audience website and is not designed for or targeted at children. BiGH does not knowingly collect, use or disseminate any personally identifiable information from children under the age of 13. If we become aware of personally identifiable information regarding a child under the age of 13, we will use such information for the sole purpose of contacting a parent or guardian to obtain verifiable parental consent. If we cannot do so after a reasonable period of time, we will make reasonable efforts to delete it from our records. Upon request from the parent or guardian, we will provide a description of the specific types of personally identifiable information that may have been collected.",
        ),
      ],
    },
    {
      heading: "7. Third-party links",
      blocks: [
        p(
          "The Site may contain links to websites operated and maintained by third parties over which we have no control. Any information you provide to third-party websites will be governed under the terms of each website’s privacy policy, and we encourage you to investigate and ask questions before disclosing any information to the operators of third-party websites. We have no responsibility or liability whatsoever for the content, actions or policies of third-party websites. The inclusion of third-party websites on our Site in no way constitutes an endorsement of such websites’ content, actions or policies.",
        ),
      ],
    },
    {
      heading: "8. Complaints",
      blocks: [
        p(
          "BiGH takes your privacy seriously. If you believe we have not complied with this Privacy Notice, please contact us so we can investigate your complaint. Please send your questions or complaints to:",
        ),
        { kind: "address", lines: [...ADDRESS, "support@bighnow.com"] },
      ],
    },
  ],
};

export const returns: LegalDoc = {
  slug: "returns",
  title: "Return Policy",
  description: "45 days to decide: how returns and refunds work at BiGH.",
  updated: "November 16, 2026",
  sections: [
    {
      blocks: [
        p(
          "We proudly stand behind our products. If you are not satisfied with a product within 45 days of purchase, we will refund your purchase, no questions asked. Please note that shipping costs associated with the purchase are not part of the refund.",
        ),
      ],
    },
    {
      heading: "Refunds after 45 days",
      blocks: [
        p(
          "After 45 days, if your product is unused and in the same condition that you received it, we will offer you a refund within a year of purchase (shipping costs associated with the purchase are not part of the refund). To be eligible for this refund, send us the unopened products. After checking their condition, we will email you to let you know that we have received your returned item, and whether your refund is approved. If it is approved, a credit will be applied to your credit card or original method of payment.",
        ),
      ],
    },
    {
      heading: "Refund not received",
      blocks: [
        p(
          "If you haven’t received your refund, please check your bank account again. Then contact your credit card company: it may take some time before your refund is officially processed. If you have done all of this and you still have not received your refund, please email us at support@bighnow.com.",
        ),
      ],
    },
    {
      heading: "Exchanges",
      blocks: [
        p(
          "We only replace products if they are defective or damaged. If you need to exchange an item, please email us at support@bighnow.com or call 800-919-2089, and send your item to the address below.",
        ),
      ],
    },
    {
      heading: "Where to send returns and exchanges",
      blocks: [
        p(
          "Please put your name and order number inside the package, so we can find your order quickly.",
        ),
        { kind: "address", lines: ADDRESS },
      ],
    },
  ],
};

export const terms: LegalDoc = {
  slug: "terms",
  title: "Terms and Conditions",
  description: "The terms for using the BiGH website and buying from BiGH.",
  updated: "November 16, 2026",
  sections: [
    {
      blocks: [
        p(
          "This website, mobile application, and/or electronic service (collectively, the “Services”) is owned and operated by BiGH Corporation and/or its subsidiaries or affiliates (“Company,” “we,” or “us”). These Terms and Conditions (“Terms”) apply to your use of the Services or other websites, mobile applications, or electronic services on which these Terms are posted.",
        ),
        p("Please read these Terms carefully before using any Services."),
        p(
          "The Company offers the Services conditioned upon your acceptance of these Terms, and your continued use of the Services constitutes your agreement to these Terms. If you do not wish to be bound by these Terms, do not access or use the Services.",
        ),
        p(
          "Note that special terms apply to some features offered through certain Services, like subscription-based services, rules for particular contests or sweepstakes or other features or activities. These terms are posted in connection with the applicable service or product offering. Any such terms are in addition to these Terms, and in the event of a conflict, prevail over these Terms.",
        ),
        p(
          "You acknowledge that these Terms are supported by reasonable and valuable consideration, the receipt and adequacy of which are hereby acknowledged. Without limiting the generality of the foregoing, you acknowledge that such consideration includes your use of the Services and receipt of data, materials and information available at or through the Services, the possibility of our use or display of User Submissions (as defined below) and the possibility of the publicity and promotion from our use or display of User Submissions.",
        ),
      ],
    },
    {
      heading: "Your license to access and use the Services, and ownership",
      blocks: [
        p(
          "The content, information, software, designs, materials, functions and data included in and contained on the Services (the “Content”) are protected by intellectual property and other laws. You must comply with these and any other applicable laws when you use the Services.",
        ),
        p(
          "Unless indicated to the contrary and subject to your strict compliance with these Terms, you may access and use the Services only for personal, non-commercial use, or in connection with your authorized purchase or sale of our products. In connection with these uses, Company grants you a limited, non-exclusive, revocable, non-assignable, personal and non-transferable license to access, copy, download, display, view, use, play and/or print one (1) copy of the Content made available on the Services on a personal computer, mobile phone or other wireless device, or other Internet-enabled device (each, an “Internet Device”), provided that you: (a) keep intact all copyright and other proprietary notices, (b) make no modifications to the Content, and (c) do not use the Content in a manner that suggests an association with any of our products, services or brands. Any business use, “re-mailing” or high-volume or automated use of Services is prohibited.",
        ),
        p(
          "In the event that we offer downloads of software on a Service and you download such software, the software, including any files, images incorporated in or generated by the software, and data accompanying the software (collectively, the “Software”) are licensed to you by us or third-party licensors for your personal, non-commercial use only. Your use of the Software may be governed by additional terms, which may be included with the Software. Please carefully read any additional terms to determine the full extent of conditions governing the use of such Software. We do not transfer title to the Software to you. You may not copy, reproduce, distribute or otherwise exploit the Software or decompile, reverse engineer, disassemble or otherwise reduce the Software to a human-readable form. Note that if you install certain applications that may be available via the Services, you consent to the download of Software to your Internet Device and accept these Terms and any additional terms related to such application.",
        ),
        p(
          "We reserve all rights in the Content and the Services that we do not specifically grant in these Terms. Without limitation, you may not modify, distribute, transmit, perform, broadcast, publish, license, reverse engineer, transfer or sell, or create derivative works from, the Services or any Content unless you obtain our prior written approval. You also may not use the Services in a way that could harm us or any third party. For example, you may not use the Services in a way that could:",
        ),
        list(
          "damage or interfere with the proper working of the Services;",
          "intercept any Content or information that we have not intentionally made available to you or defeat any access controls that we have implemented;",
          "give you access to the Services or Content using any interface other than the interface that we provide, or attempt to “scrape” or “harvest” Content, except if you use a “robot” program in connection with a bona fide internet search engine and we do not instruct you not to access the Services using that program;",
          "frame the Services, display any Content in connection with an unauthorized logo or mark, or do anything that could suggest falsely a relationship between us and any other party;",
          "convey unauthorized claims about the curative or health-enhancing effects of our products or suggest that we have made such claims; or",
          "otherwise adversely impact the operation of the Services, the Company, or any third party.",
        ),
        p(
          "In addition to our other legal rights, we may limit or terminate your license to use the Services, or certain features of the Services, at any time and for any reason, without prior notice to you, including our belief that you violated these Terms.",
        ),
      ],
    },
    {
      heading: "Registration and access restrictions",
      blocks: [
        p(
          "You may be required to register for an account with us in order to use certain features of the Services. If you elect to take advantage of such features, you must register through the Services by completing the applicable registration form to create your account with a unique username and password. The decision to provide this information is purely optional; however, if you elect not to provide such information, you may not be able to access certain Content or participate in certain features of the Services. You agree to: (a) provide true, accurate, current and complete information about yourself when we request it; (b) maintain and promptly update this information to keep it true, accurate, current and complete to the extent the Services permit such updates; (c) use limited-access portions of the Services only using access credentials that we have issued to you; and (d) exit your account at the end of each session in which you have logged in to the Services.",
        ),
        p(
          "You must maintain the confidentiality of any access credentials that we issue to you and may not share them with any other person. You must notify the Company immediately of any unauthorized use of your credentials or any other breach of security. Even if you notify us, you will be responsible for any activities that occur using your access credentials, including any charges resulting from the use of your account.",
        ),
      ],
    },
    {
      heading: "No professional advice or medical information",
      blocks: [
        p(
          "The Services do not provide medical advice, diagnosis or treatment, and the information included on the Services is offered for informational purposes only. Some portions of the Services may allow you to submit questions either to us or to third parties who have agreed to communicate with our users. Although we provide information about our products through the Services, neither our employees nor these third parties are authorized to provide medical or other professional advice through the Services. We also have not confirmed the qualifications of any third party who provides information through the Services, even if that third party lists his or her qualifications. As a result, you should never use the information you obtain on the Services for diagnosis or treatment of any health problem or in place of any medication or other treatment prescribed by a physician or other healthcare provider.",
        ),
        p(
          "Please consult with your physician or other healthcare provider if you have health-related questions before using any of our products or relying on any information you obtain on the Services. You should discuss any medications or nutritional supplements you are using with a healthcare provider before using any new medications or supplements.",
        ),
        p(
          "The statements on the Services have not been evaluated by the Food and Drug Administration. Our products are not intended to diagnose, treat, cure, or prevent any disease.",
        ),
      ],
    },
    {
      heading: "User Submissions",
      blocks: [
        p(
          "The Services may allow you to submit, embed, display, transmit, or otherwise distribute audio, video, text, or other materials (collectively, “User Submissions”) to or through the Services. When you provide User Submissions, you grant to the Company a non-exclusive, royalty-free, fully paid, perpetual, worldwide, irrevocable and fully sublicensable and transferable (in whole or in part) license under all copyrights, trademarks, patents, trade secrets, privacy and publicity rights and other intellectual property rights you own or control to: (i) use, reproduce, transmit, modify, index, adapt, publish, translate, create derivative works from, distribute, display and otherwise exploit such content throughout the world in any media, whether now known or hereafter invented, including for any and all purposes, including commercial or marketing purposes, all without further notice to you, with or without attribution, and without the requirement of any permission from or payment to you or any other person or entity, and (ii) to use your name, persona or likeness alone or in connection with such uses, without any obligation or remuneration to you. Without limitation, the granted rights include the right to: (a) configure, host, index, cache, archive, store, digitize, compress, optimize, modify, reformat, edit, adapt, publish in searchable format, and remove such User Submissions and combine same with other materials, and (b) use any ideas, concepts, know-how, or techniques contained in any User Submissions for any purposes whatsoever, including developing, manufacturing, and marketing products and/or services. Except as prohibited by law, you hereby waive, and you agree to waive, any moral rights (including attribution and integrity) that you may have in any User Submissions, even if it is altered or changed in a manner not agreeable to you. To the extent not waivable, you irrevocably agree not to exercise such rights (if any) in a manner that interferes with any exercise of the granted rights. You understand that you will not receive any fees, sums, consideration, or remuneration for any of the rights granted in this section.",
        ),
        p(
          "Except as provided in our Privacy Notice, we do not guarantee that User Submissions will be private, even if the User Submission is in a password-protected area. Accordingly, you should not provide User Submissions that you want protected from disclosure. Except as otherwise described in the Privacy Notice, you agree that: (a) your User Submissions will be treated as non-confidential, regardless of whether you mark them “confidential,” “proprietary,” or the like, and will not be returned, and (b) Company does not assume any obligation of any kind to you or any third party with respect to your User Submissions. Upon Company’s request, you will furnish us with any documentation necessary to substantiate the rights to such content and to verify your compliance with these Terms. You acknowledge that the Services may be subject to breaches of security and that you are aware that submissions of User Submissions may not be secure, and you will consider this before submitting any User Submissions.",
        ),
        p(
          "In your communications with Company, please keep in mind that the Company does not accept or consider any unsolicited ideas or materials for products or services, or even improvements to products or services, such as ideas, concepts, inventions, books, etc. (collectively, “Unsolicited Ideas and Materials”). Any Unsolicited Ideas and Materials you post on or send to us via the Services are deemed User Submissions and licensed to us as set forth above. In addition, Company retains all of the rights held by members of the general public with regard to your Unsolicited Ideas and Materials. The Company’s receipt of your Unsolicited Ideas and Materials is not an admission by Company of their novelty, priority, or originality, and it does not impair the Company’s right to contest existing or future intellectual property rights relating to your Unsolicited Ideas and Materials. Notwithstanding any custom and practice to pay an individual for an idea (if any), nothing herein shall create an implied or express contract to compensate entrants for their Unsolicited Ideas and Materials and there is no obligation for Company to pay or otherwise compensate you for any of your ideas or materials in any communications with us, whatsoever.",
        ),
        p(
          "By providing User Submissions through the Services, you represent, warrant and covenant that you own those User Submissions or otherwise have the right to grant to us the rights described in this section. You further represent, warrant and covenant that the User Submissions:",
        ),
        list(
          "will be accurate and will comply with these Terms;",
          "will be original with you or you have all necessary rights from third parties in order to post the User Submissions on our Services, without the need for any permission from or payment to any other person or entity to exploit, and to authorize us to exploit, such User Submissions in all manners contemplated by these Terms;",
          "will be respectful of others’ opinions so we can continue to offer interactive features for everyone to enjoy;",
          "will not cause injury to any person or entity, including as used by us in accordance with these Terms;",
          "will not be false, fraudulent, libelous, defamatory, sexually explicit, obscene, threatening, invasive of privacy or publicity rights, abusive, illegal or otherwise objectionable;",
          "will not constitute or encourage violence or a criminal offense, violate the rights of any party, including intellectual property rights, or otherwise give rise to liability or violate any law;",
          "will not impersonate any other person, user, or company, or be false, fraudulent, deceptive, inaccurate, or misleading, or misrepresent your identity or affiliation with a person or company;",
          "will not include other people’s personal information, such as another person’s address, phone number, email address, social security number, credit card number, medical information, financial information, or any other information that may be used to track, contact, or impersonate that individual;",
          "will not contain software viruses, Trojan horses, spyware or any other technologies or malicious code that could impact the operation of the Services or any computer or device used to access the Internet, or political campaigning, chain letters, mass mailings, or any form of “spam”; and",
          "will not advertise or promote a product or service or include advertising or other commercial material, except with our prior written consent.",
        ),
        p(
          "We may refuse or remove a User Submission without notice for any reason, including our belief that a User Submission may violate these Terms or be otherwise objectionable. However, we will have no obligation to review, monitor, display, post, store, maintain, accept or otherwise make use of User Submissions, and you agree that neither we nor our employees or agents will be liable for User Submissions or any loss or damage to you and any other person or entity resulting from User Submissions.",
        ),
        p(
          "You are solely responsible for your interaction with other users of the Services, whether online or offline. You are and shall remain solely responsible for the User Submissions you distribute on or through any Services and for the consequences of submitting and posting same. You should be skeptical about information provided by others, and you acknowledge that the use of any User Submission is at your own risk. We are not responsible or liable for the conduct of any user or content of any User Submission. We do not endorse the opinions, advice or recommendations posted or sent by users in any User Submission, and we specifically disclaim any and all liability in connection therewith. We reserve the right, but have no obligation, to monitor or become involved in disputes between you and other users. Exercise common sense and your best judgment in your interactions with others (e.g., when you submit any personal or other information) and in all of your other online activities. If you discover any content that violates these Terms, you may report it to support@bighnow.com.",
        ),
        p(
          "We cannot and do not assure that other users are or will be complying with the foregoing or any other Terms, and, as between you and us, you hereby assume all risk of harm or injury resulting from any such lack of compliance.",
        ),
      ],
    },
    {
      heading: "Links to third-party sites",
      blocks: [
        p(
          "The Services may contain links to other sites or electronic services that are not operated by our family of companies. These links are provided as a convenience to you. However, we do not represent that we have endorsed or evaluated the information on those other sites or electronic services. Your relationship with the operators of these third-party sites is governed by the terms and conditions and privacy policy, if any, of those sites, and not by these Terms. Therefore, you should review those documents before using the third-party services.",
        ),
        p(
          "Nor can we be held responsible for the accuracy, relevance, legality or decency of material contained on Services retrieved in searches and/or listed in search results or identified on search results pages.",
        ),
      ],
    },
    {
      heading: "Commercial transactions",
      blocks: [
        p(
          "The Services allow you to purchase products or services. To purchase any products or services through the Services, you must: (a) be at least eighteen years of age, (b) provide us with valid payment information associated with a credit card or other payment method that you are authorized to use, and (c) authorize us to charge your credit card or other payment method for the price of the products or services that you request, together with any taxes, fees, or shipping charges described on the Services.",
        ),
        p(
          "We stand behind the products and services that we sell, and we list the return policy that applies to purchases from the Services. In general, we accept returns for a limited period of time following a purchase, and your sole remedy if you are dissatisfied with a product that you have purchased through the Services will be to return the unused portion of the product for a refund. After the return periods described in our Return Policy have expired, all sales are final, and we will not accept returns or issue refunds.",
        ),
        p(
          "In offering product descriptions on the Services, we attempt to be accurate, but we do not warrant that any product description is accurate, complete, or error-free, nor do we represent that any product will diagnose, treat, cure, or prevent any disease. If you receive a product and believe that it materially differs from the product description, your sole remedy will be to return the product to us for a refund in conformance with the return policy listed on the Services. Likewise, we attempt to list the current price for each product that we sell, but a small number of products may be mispriced. In these cases, we will notify you of the corrected price before shipping the product and will either cancel your order or give you an opportunity to cancel your order or decide to keep your order.",
        ),
      ],
    },
    {
      heading: "Electronic communications",
      blocks: [
        p(
          "When you access or use the Services, send emails to us, or receive electronic communications from us, you are, and consent to, communicating with the Company electronically. We may communicate with you by email or by posting notices through one or more of the Services. You agree that all notices, disclosures, agreements, policies, and other communications that the Company provides to you electronically satisfy any requirement that such communications be in writing.",
        ),
      ],
    },
    {
      heading: "International orders",
      blocks: [
        p(
          "By confirming your order for shipment outside the United States, you agree to the additional terms contained in this section.",
        ),
        p(
          "If any package is returned to us because of an incorrect address, because you refuse the package, or for any reason other than our error alone, you will be responsible for our shipping cost for the return and reshipment of the package. If the cost to return the package to us exceeds the cost of the goods ordered, or if you have ordered products that we are informed cannot be imported into the country of intended delivery, we may instruct the shipping company to abandon the package, but even if we do so, you will remain responsible for payment.",
        ),
        p(
          "Additionally, you are considered the importer of record for all shipments from us, and must comply with all laws and regulations of the country of destination and all laws and regulations the United States imposes on exports to that country. You agree to pay any fees, fines, or other costs charged to us or to you in connection with any non-compliance with laws and regulations of the country of destination.",
        ),
        p(
          "If we decide to allow return of an item that has been rejected because of import or other legal compliance issues, we will refund the purchase price of the merchandise, less any charges we incurred in connection with the shipment, such as quarantine fees, exam fees, demurrage charges, or warehousing fees assessed in the destination country or in the United States upon return of the goods, and less the shipping costs to return the package to us. Supply of goods, services and software through the Services is subject to United States export control and economic sanctions requirements. By acquiring any such items through the Services, you represent and warrant that your acquisition comports with and your use of the item will comport with those requirements.",
        ),
      ],
    },
    {
      heading: "Disclaimers",
      blocks: [
        p(
          "Your use of the Services is at your sole risk. The Services are provided on an “as is” and “as available” basis. We reserve the right to restrict or terminate your access to the Services or any feature or part thereof at any time. We expressly disclaim all warranties of any kind, whether express or implied, including the implied warranties of merchantability and fitness for a particular purpose and any warranties that materials on the Services are non-infringing, as well as warranties implied from a course of performance or course of dealing; that access to the Services will be uninterrupted or error-free; that the Services will be secure; that the Services or the servers that make the Services available will be virus-free or otherwise free of harmful components; or that information on the Services will be complete, accurate or timely. If you download any materials from the Services, you do so at your own discretion and risk. You will be solely responsible for any damage to your computer system or loss of data that results from the download of any such materials. No advice or information, whether oral or written, obtained by you from us or through or from the Services will create any warranty of any kind. We do not make any warranties or representations regarding the use of the materials on the Services in terms of their completeness, correctness, accuracy, adequacy, usefulness, timeliness, reliability or otherwise.",
        ),
        p(
          "In certain states, the law may not permit the disclaimer of warranties, so the above disclaimer may not apply to you.",
        ),
      ],
    },
    {
      heading: "Limitation of liability",
      blocks: [
        p(
          "To the greatest extent permitted by applicable law, neither we, nor our suppliers or third-party content providers, will be liable for any direct, indirect, punitive, exemplary, incidental, special, consequential or other damages arising out of or in any way related to: (1) the Services (including any delay or inability to use the Services), (2) any information, products or services advertised in or obtained through the Services, or (3) our removal or deletion of any materials submitted or posted on the Services, whether based on contract, tort, strict liability or otherwise, even if we or any of our suppliers have been advised of the possibility of damages.",
        ),
        p(
          "We each agree that any dispute proceedings will be conducted only on an individual basis and not in a class, consolidated or representative action.",
        ),
        p(
          "Your sole and exclusive remedy for any claims or disputes involving us that are not waived by these Terms will be to discontinue your use of the Services and to seek a refund of the money you paid to us, if any, during the three months preceding your initiation of the claim or dispute. (Such a refund, in any case, will be governed by the applicable refund policy and the terms of sale specified on the Services or in these Terms.)",
        ),
        p(
          "The limitations, exclusions and disclaimers in this section and elsewhere in these Terms apply to the maximum extent permitted by applicable law.",
        ),
      ],
    },
    {
      heading: "Indemnification",
      blocks: [
        p(
          "You agree to indemnify, defend and hold harmless the Company and its officers, directors, employees, contractors, agents, licensors, service providers, subcontractors and suppliers from and against any and all losses, liabilities, expenses, damages and costs, including reasonable attorneys’ fees and court costs, arising from or in connection with your use of the Services or our products or services or any violation or alleged violation by you of these Terms or applicable law. We reserve the right, at our own expense, to assume exclusive defense and control of any matter otherwise subject to indemnification by you and, in such case, you agree to cooperate with us in the defense of such matter. You may not settle any claim covered by this section or admit any liability on the part of the Company without the Company’s prior written approval.",
        ),
      ],
    },
    {
      heading: "Jurisdiction and venue",
      blocks: [
        p(
          "The laws of the State of California govern these Terms and any dispute of any sort that may arise between you and the Company or its affiliates, without regard to conflict of laws rules, as if entered into by residents of California and fully performed therein. You irrevocably consent to the jurisdiction of the state and federal courts located in or serving Los Angeles County, California for any action relating to the Services or these Terms. Notwithstanding any other provision of these Terms, we may seek injunctive or other equitable relief from any court of competent jurisdiction.",
        ),
        p(
          "Regardless of any statute or law to the contrary, you must file any claim or action related to use of the Services or these Terms within one year after such claim or action accrued. Otherwise, you will waive the claim or action.",
        ),
        p(
          "We make no representation that Content on any Services is appropriate or available for use in any particular location. Those who choose to access the Services do so on their own initiative and are responsible for compliance with all applicable laws, including any applicable local laws.",
        ),
      ],
    },
    {
      heading: "Changes to these Terms",
      blocks: [
        p(
          "We reserve the right, in our sole discretion, to change these Terms at any time by posting revised terms on the Services. It is your responsibility to check periodically for any changes we may make to these Terms. Your continued use of the Services following the posting of changes to these terms or other policies means you accept the changes.",
        ),
      ],
    },
    {
      heading: "Termination",
      blocks: [
        p(
          "These Terms constitute an agreement between you and the Company, which the Company may terminate in its sole discretion, in whole or in part, at any time and for any reason. If the Company terminates this agreement with you, you may no longer access the Services. Upon termination of this agreement and/or your access to the Services, you will immediately destroy any copies of any Content, whether in printed or software format. Otherwise applicable portions of these Terms survive termination of these Terms, including applicable portions of the sections relating to No Professional Advice or Medical Information; User Submissions; Links to Third-Party Sites; Electronic Communications; Disclaimers; Limitation of Liability; Indemnification; Jurisdiction and Venue; Termination; and Entire Agreement, Severability, No Waiver.",
        ),
      ],
    },
    {
      heading: "Entire agreement; severability; no waiver",
      blocks: [
        p(
          "These Terms, together with the Privacy Notice incorporated within them by reference and any policies that we post on the Services, constitute the entire agreement of the parties with respect to the subject matter hereof and supersede all prior or contemporaneous communications and proposals, whether oral or written, between the parties with respect to such subject matter. If any provision of these terms is deemed unlawful, void or unenforceable, the remaining provisions will remain in place and the invalidated provision will be deemed replaced by an enforceable provision that most closely reflects the intent of the parties.",
        ),
        p(
          "Our failure to exercise or enforce any right or provision in these Terms will not constitute a waiver of that right or provision or any other rights or provisions included within the Terms.",
        ),
      ],
    },
    {
      heading: "How to contact us",
      blocks: [
        p(
          "If you have any questions or comments about these Terms or the Site, please email us at support@bighnow.com, call 800-919-2089, or write to:",
        ),
        {
          kind: "address",
          lines: [...ADDRESS.slice(0, 1), "Attn: Legal Department", ...ADDRESS.slice(1)],
        },
      ],
    },
  ],
};

export const legalDocs = { privacy, terms, returns } as const;
