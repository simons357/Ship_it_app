# Ship It — Help

Ship It lets you manage what you put on GitHub without opening the GitHub website. Use this guide to get set up, ship files, and fix common problems.

---

## What Ship It does

Ship It is a simple way to:

- Connect your GitHub account
- Choose a repository
- Add, update, or remove files
- Leave a clear commit message for each change

You stay in one place instead of jumping around on github.com.

---

## Getting started

### 1. Sign in with GitHub

1. Open Ship It.
2. Choose **Sign in with GitHub**.
3. Approve access when GitHub asks.
4. Return to Ship It — your account should appear as connected.

**Tip:** If sign-in fails, close the browser window GitHub opened, then try again. Check that you’re signed into the correct GitHub account.

### 2. Choose a repository

1. After sign-in, open your list of repositories.
2. Pick the repo you want to update.
3. Confirm you’re on the right branch (usually `main` or `master`).

### 3. Ship your first change

1. Select files from your device (or drag them in, if your app supports it).
2. Choose where they should live in the repo (folder + file name).
3. Write a short commit message that describes the change.
4. Tap **Ship** / **Upload**.
5. Wait for confirmation that the commit landed on GitHub.

---

## Everyday tasks

### Upload a new file

1. Open the target repository.
2. Go to the folder where the file should live (or create the path).
3. Add the file from your device.
4. Enter a commit message (for example: `Add product wallpaper assets`).
5. Ship the change.

### Update a file that already exists

1. Open the repository and find the existing file.
2. Choose **Replace** / **Update** and pick the new version from your device.
3. Write a commit message that says what changed.
4. Ship — Ship It updates the file in place on GitHub.

### Delete a file

1. Open the repository and select the file.
2. Choose **Delete**.
3. Confirm and add a commit message (for example: `Remove unused icon`).
4. Ship the deletion.

### Switch repositories

Use the repository picker at the top of the app to jump between repos you can access. Changes always go to the repo you currently have selected.

---

## Commit messages that help

Good messages make history readable for you and anyone else on the repo:

| Prefer | Avoid |
| --- | --- |
| `Add desktop wallpaper assets` | `update` |
| `Fix icons for App Store listing` | `stuff` |
| `Remove old JPG mockup` | `asdf` |

Keep messages short, specific, and in the present tense.

---

## GitHub access & permissions

Ship It needs permission to read your repositories and write file contents. Typical scopes include:

- Read your profile and repositories
- Create commits (add / update / delete files)

If you can’t see a private repo, check that:

1. You’re signed into the right GitHub account.
2. Ship It’s GitHub authorization still includes that repo (or org).
3. Your GitHub role on that repo allows writing contents.

You can revoke access anytime in GitHub: **Settings → Applications → Authorized OAuth Apps** (or **Authorized GitHub Apps**), then find Ship It and revoke it.

---

## Troubleshooting

### “Sign in failed” or the GitHub window closes with an error

- Confirm you have an internet connection.
- Try signing out of GitHub in the browser, then sign in again through Ship It.
- Make sure GitHub isn’t blocking third-party / app authorization for your org.

### “Permission denied” when shipping

- You may only have read access to that repository. Ask a repo admin for write access, or pick a repo you own.
- Org SSO may require you to authorize Ship It again after enabling SSO.

### Upload never finishes

- Large files take longer; wait for confirmation before leaving the screen.
- Retry on a stronger connection.
- If the same file fails twice, check that the path doesn’t conflict with an existing folder name (or the other way around).

### I don’t see my new commit on GitHub

1. Refresh the repository page on GitHub.
2. Confirm you’re looking at the same branch Ship It used.
3. In Ship It, check the last ship status / activity for a success message or error.

### I shipped to the wrong place

You can’t undo a commit from Ship It’s help screen alone. Options:

- Ship a follow-up change that fixes or replaces the files.
- On GitHub, revert the commit (or restore the previous file version) if you have access.

---

## Privacy & safety

- Ship It only changes repositories you authorize and select.
- Don’t ship secrets (API keys, passwords, private keys) into public repos.
- Prefer private repositories for unpublished or sensitive content.
- Revoke Ship It’s GitHub access if you stop using the app.

---

## FAQ

**Do I still need to use the GitHub website?**  
For everyday file uploads and updates, no — that’s what Ship It is for. You may still use GitHub for pull requests, issues, or advanced git workflows.

**Can I use Ship It with organization repos?**  
Yes, if your GitHub account has access and you’ve granted Ship It permission to those repos (and completed org SSO authorization if required).

**Does Ship It replace git?**  
No. Ship It is for simple content management on GitHub. Full branching, merging, and local development still work best with git tools.

**Where are my files stored?**  
On GitHub, in the repository and path you choose — not as a permanent mirror only inside Ship It.

**How do I get more help?**  
Open an issue in this repository describing what you tried and what went wrong (include screenshots when you can).

---

## Quick reference

| Goal | Steps |
| --- | --- |
| First setup | Sign in → pick repo → ship a file |
| Add file | Repo → folder → add file → commit message → Ship |
| Replace file | Find file → update → commit message → Ship |
| Remove file | Find file → delete → commit message → Ship |
| Fix access | Check GitHub app permissions / repo write access |

Welcome aboard — ship something.
