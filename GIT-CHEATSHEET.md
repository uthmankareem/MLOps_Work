# Git & GitHub Cheat Sheet (Stage 1)

**For:** clever-tinkerer-6320 · MLOps course
**Checklist coverage:** every command from Stage 1 so far, with what each part means and what happens if you skip it.

---

## The mental model
```
  YOUR laptop                     GitHub (origin)
 [local repo]  ←pull/push→  [MLOps_Work (remote)]
```
- **Local repo** = the `.git` + your working files on this machine.
- **Origin** = GitHub nickname for the remote repo.
- Git tracks **your commits locally first**, then `push` uploads them.

---

## Commands & what each part means

### 1. Configure identity (do once per machine)
```powershell
git config --global user.name "uthmankareem"
git config --global user.email "kareemuthman305@gmail.com"
```
| Part | Meaning |
|---|---|
| `git` | The version-control program |
| `config` | Work with Git settings |
| `--global` | Apply to every repo on this machine |
| `user.name` / `user.email` | The settings being set |
| `"..."` | The value (quote it) |

**If skipped:** Git refuses to commit ("Please tell me who you are").

### 2. Verify settings
```powershell
git config --global --list
```
Shows all global settings. `--list` = print them.

### 3. Clone (copy remote → local, once per repo)
```powershell
git clone https://github.com/uthmankareem/MLOps_Work.git
```
| Part | Meaning |
|---|---|
| `clone` | Copy a remote repo to your machine |
| `https://github.com/...` | The repo's URL |
| `uthmankareem` | GitHub username (owner) |
| `MLOps_Work` | Repo name |
| `.git` | Signals it's a Git URL |

**If URL wrong:** "Repository not found" error.

### 4. Check the working state
```powershell
git status
```
Shows branch, staged/untracked files. **Run before committing.**

### 5. Stage a file
```powershell
git add README.md
```
| Part | Meaning |
|---|---|
| `add` | Move the file into the **staging area** (mark for commit) |
| `README.md` | File to stage |

**If skipped:** file stays *untracked* and is ignored by Git — never committed.

*(To stage everything: `git add .`)*

### 6. Save a snapshot
```powershell
git commit -m "Add README"
```
| Part | Meaning |
|---|---|
| `commit` | Save the staged snapshot into history |
| `-m` | "Message" flag |
| `"Add README"` | The commit message |

**If no `-m`:** Git opens an editor to ask for a message; without one it aborts.

### 7. Upload to GitHub
```powershell
git push origin main
```
| Part | Meaning |
|---|---|
| `push` | Upload local commits to the remote |
| `origin` | Default nickname for the remote repo |
| `main` | The branch you're pushing |

**If not pushed:** commit exists only on your laptop — not on GitHub.

### 8. Get the latest from GitHub (coming next)
```powershell
git pull
```
Download remote commits to your local repo.

---

## Quick glossary
| Term | Meaning |
|---|---|
| `git` | The program |
| repo | A project folder under version control |
| commit | A saved snapshot of changes |
| staging area | The "to-be-committed" tray |
| `add` | File → staging area |
| `commit` | Staging area → permanent history |
| `push` | Local → remote |
| `pull` | Remote → local |
| `clone` | Create a local copy of a remote repo |
| `origin` | Nickname for the remote repo |
| `main`/`master` | Default branch (trunk) |
| branch | A separate line of development |
| `-m` | Message flag |
| `--global` | Applies machine-wide |
| untracked | File Git sees but isn't tracking yet |

---

## Next steps (Stage 1 continued)
- Finish `git push origin main`
- Add collaborators (me) to the repo
- Branching → merging → conflict → pull request

*Save for reference. Print-friendly: 1-2 pages.*