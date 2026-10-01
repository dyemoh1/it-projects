# Project Desk — Firebase web application

A portfolio edition of a coursework project manager. The supplied coursework contained Google sign-in and Firestore CRUD. This edition was rewritten with AI assistance to render user input as text, remove credential logging, correct form events, and scope records to `/users/{uid}/projects`.

## Local setup

1. Use a separate Firebase development project. Register a web app, enable Google Authentication, and create a Firestore database.
2. Copy `config.example.js` to `config.js` and fill in your web app configuration.
3. Deploy the supplied `firestore.rules` to that development project. These rules restrict each user's records to their authenticated UID.
4. Serve this directory locally with `python -m http.server 8000`. Authorize the local domain in Firebase Authentication as required by your project settings.
5. Open `http://localhost:8000/firebase.html`.

The unconfigured page displays a setup message; it is not a live connected demo. Existing coursework records under the old shared `projects` collection are not migrated or accessed by this edition.

## Validation before deploying

- Sign in and create, edit, and delete a synthetic project.
- Sign out and verify that the project list and form disappear.
- Use a second test account to verify records remain separate.
- Test unauthenticated and cross-user requests against the Firestore rules using the Firebase emulator or rules simulator.
- Enter HTML characters and verify that they display as text.
- Test rejected writes and network failures.

Cloud integration and rules enforcement have **not** been executed or verified during preparation. No credentials, real user records, or original Firebase configuration are published. Firebase browser configuration is not an authorization mechanism; deployed rules enforce access.

## Attribution

Based on David Yemoh's coursework files, which include a mixture of starter material and personal contributions. Individual historical contributions are uncertain. The portfolio rewrite and security improvements were AI-assisted; no claim of entirely independent authorship is made.
