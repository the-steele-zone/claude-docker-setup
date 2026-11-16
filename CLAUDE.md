# MeshTool — Pending Tasks

Before the GitHub App flow goes live, complete these 5 steps in order:

- [ ] **1. Generate GitHub App private key**
  Go to github.com/settings/apps/meshtool → "Generate a private key" → download `.pem`
  Add as `GITHUB_PRIVATE_KEY` env var in Railway (thinkzone-api) and Vercel (meshtool-app)

- [ ] **2. Set remaining GitHub App env vars** in Railway and Vercel
  ```
  GITHUB_APP_ID=<see vault>
  GITHUB_CLIENT_ID=<see vault>
  GITHUB_CLIENT_SECRET=<see vault>
  GITHUB_WEBHOOK_SECRET=<see vault>
  ```
  Railway account API token for variable management: see vault (`RAILWAY_ACCOUNT_TOKEN`)
  Vault location: C:\Users\vipth\.vault\secrets.env (never commit)

- [ ] **3. Upgrade Clerk from test → production**
  dashboard.clerk.com → switch meshtool-app to production
  Update `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` in Vercel with `pk_live_` / `sk_live_` keys

- [ ] **4. Merge PR #20** in think-zone/creator-os
  https://github.com/think-zone/creator-os/pull/20
  Railway and Vercel redeploy automatically on merge

- [ ] **5. Test the full install flow**
  Install MeshTool GitHub App on a test account → GitHub fires webhook to
  `https://api.meshtool.ai/webhook/github` → API key provisioned → GitHub redirects
  to `https://meshtool.ai/setup?installation_id=...` → developer sees their key
