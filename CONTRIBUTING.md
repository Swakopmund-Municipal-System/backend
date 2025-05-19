# Backend Team Git Workflow Guide  
These guidelines outline the Git workflow that the Backend Team must follow to ensure a structured and efficient development process. The goal is to keep our `dev` branch stable while maintaining a clear feature and bug-fix workflow.

## 1. Creating Issues on GitHub
Team leads are responsible for creating GitHub issues for every new feature. Here’s how:

1. Go to your **project repository** on GitHub.
2. Navigate to the **Issues** tab and create a new issue.
3. The issue **name** must follow this format:
   ```
   feature-(name-of-feature)
   ```
   **Example:** `feature-user-authentication`
4. Assign the issue to the **team member** responsible for the feature.

## 2. Branching Strategy
Once an issue is assigned, the responsible team member must:

1. Create a **new branch** from the issue.
2. The branch name should be the **same as the issue name**:
   ```
   feature-(name-of-feature)
   ```
3. **Example:** If the issue is `feature-user-authentication`, the branch should be:
   ```
   git checkout -b feature-user-authentication
   ```
4. Make sure the branch is based on the **latest `dev` branch**.

## 3. Keeping the Feature Branch Updated
To avoid conflicts and ensure a smooth merge:

1. Before starting work, always pull the latest `dev` branch:
   ```
   git checkout dev
   git pull origin dev
   ```
2. Switch back to your feature branch and update it:
   ```
   git checkout feature-user-authentication
   git merge dev
   ```
3. After completing your work, **update your branch again with the latest `dev`** before pushing:
   ```
   git pull origin dev
   git merge dev
   ```

## 4. Pushing and Making a Pull Request (PR)
Once the work is done:

1. Push the feature branch to GitHub:
   ```
   git push origin feature-user-authentication
   ```
2. Go to GitHub and create a **Pull Request (PR)** to merge your feature branch into `dev`.
3. Assign the PR to your **team lead** for review.
4. The team lead must review the code and, once approved, **merge it into `dev`**.
5. **Important:** Do NOT merge into `main` yet.

## 5. Merging to Main at Sprint End
At the **end of the sprint**, once all features are merged into `dev`:

1. Ensure `dev` is **fully stable**.
2. Only then, merge `dev` into `main`.
3. This ensures `main` remains stable and only receives tested, sprint-complete features.

## 6. Handling Hotfixes
If a bug is found in `dev` at the end of a sprint:

1. Create a **hotfix branch**:
   ```
   git checkout -b hotfix-(fix-name)
   ```
   **Example:** `hotfix-login-error`
2. Apply the fix, then push and merge the **hotfix branch into `dev`**.

If you have any questions, **follow this guide first before asking**. Let's keep our process clean and efficient!
