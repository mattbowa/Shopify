# 🧠 Shopify SEO Checker App (FastAPI)

A lightweight Shopify app built with **FastAPI** that connects to a Shopify store, authenticates via OAuth, and retrieves theme data for SEO auditing and analysis.

---

## 🚀 Features

- Secure **Shopify OAuth 2.0** installation
- Read Shopify theme files and content
- Inspect SEO elements (titles, meta tags, alt text, etc.)
- Built with **FastAPI + HTTPX**
- Persistent token storage with **SQLite**

---

## 🧩 Prerequisites

Before you start, you’ll need:

- A **Shopify Partner account** → [https://partners.shopify.com](https://partners.shopify.com)
- A **Shopify development store**
- **Python 3.9+**
- **ngrok** (for HTTPS tunneling to your localhost)

---

## 🏗️ 1. Create a New Shopify App

1. Log into your **Shopify Partner Dashboard**
2. Go to **Apps → Create app**
3. Select **Custom App → Build for a client’s store** (or your dev store)
4. Fill in:

   | Field | Example |
   |--------|----------|
   | App name | SEO Checker |
   | App URL | `https://<your-ngrok-url>` |
   | Allowed redirection URL | `https://<your-ngrok-url>/auth/callback` |

5. After creating it, copy:
   - `API key`
   - `API secret key`

You’ll use these in your `.env` file.

---

## ⚙️ 2. Environment Setup

Clone the project and create a `.env` file:

```bash
git clone https://github.com/yourusername/shopify-seo-checker.git
cd shopify-seo-checker
touch .env
```

Then add:

```env
SHOPIFY_API_KEY=your_api_key_here
SHOPIFY_API_SECRET=your_secret_here
APP_URL=https://your-ngrok-url
```

---

## 🐍 3. Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv httpx
```

*(SQLite is included with Python by default.)*

---

## 🧠 4. Start the Server

```bash
uvicorn main:app --reload
```

This runs the FastAPI app at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 🌐 5. Expose via ngrok

Run ngrok in another terminal:

```bash
ngrok http 8000
```

You’ll get a public HTTPS URL, e.g.:

```
https://1234abcd.ngrok.io
```

Update your `.env` and Shopify App settings to match this URL:
```
APP_URL=https://1234abcd.ngrok.io
```

---

## 🔑 6. Install the App on a Store

Visit:

```
https://<your-ngrok-url>/install?shop=<your-store>.myshopify.com
```

Approve the permissions on Shopify’s screen.  
After approval, you should see a success message:
```
{"message": "App installed!", "shop": "your-store.myshopify.com"}
```

---

## 🧾 7. Test the API

Use Postman or your browser:

```bash
GET https://<your-ngrok-url>/themes?shop=<your-store>.myshopify.com
```

✅ Expected result:
```json
{
  "themes": [
    {
      "id": 123456789,
      "name": "Dawn",
      "role": "main"
    }
  ]
}
```

---

## 💾 Persistent Token Storage

The app uses **SQLite** (`sessions.db`) to store access tokens across restarts:

```python
def save_token(shop, token):
    conn = sqlite3.connect("sessions.db")
    ...
```

This ensures the “Shop not authenticated” error doesn’t occur after restarting the server.

---

## 🧱 Project Structure

```
shopify-seo-checker/
├── main.py         # FastAPI app
├── sessions.db     # Token storage (auto-created)
├── .env            # Environment variables
├── requirements.txt (optional)
└── README.md
```

---

## 🔍 8. Example API Endpoints

| Endpoint | Description | Auth Required |
|-----------|-------------|---------------|
| `/` | Health check | ❌ |
| `/install?shop=...` | Start OAuth flow | ❌ |
| `/auth/callback` | Receive OAuth token | ❌ |
| `/themes?shop=...` | Get theme list | ✅ |
| `/theme-asset?shop=...&theme_id=...&asset_key=...` | Get a theme file’s content | ✅ |

---

## 🧰 9. Example Asset Fetch

```bash
GET /theme-asset?shop=your-store.myshopify.com&theme_id=123456789&asset_key=layout/theme.liquid
```

Response:
```json
{
  "asset_key": "layout/theme.liquid",
  "content": "<!doctype html>...",
  "okay": "ok2"
}
```

---

## 🔒 10. Adding More Scopes (Optional)

If you plan to check SEO on products or collections:

```python
scopes = "read_themes,read_content,read_products,read_collections,read_files"
```

Then reinstall the app.

---

## 🧠 Next Steps

- Analyze `theme.liquid`, `settings_data.json`, and pages for:
  - `<title>` and `<meta>` tags
  - Image `alt` attributes
  - JSON-LD structured data
- Add a front-end (Shopify App Bridge + React or Polaris UI)
- Create a background job to scan SEO content automatically

---

## 💡 Troubleshooting

| Error | Cause | Fix |
|--------|--------|-----|
| `invalid_request: redirect_uri must match` | Shopify app redirect doesn’t match your ngrok URL | Update **App URL** and **Redirect URI** in Shopify |
| `Shop not authenticated` | Token missing (after restart or typo in `shop` param) | Reinstall app or persist token |
| `401 Unauthorized` | Token invalid or expired | Reinstall app |

---

## 🧑‍💻 Author

**Matt Bow**  
Built with ❤️ using **FastAPI** and **Shopify REST API**.

---

## 🪪 License

MIT License — free to use and modify.


https://9c536b8eb144.ngrok-free.app/install?shop=seo-checker-2.myshopify.com