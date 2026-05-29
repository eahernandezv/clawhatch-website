const AB_COOKIE = 'clawhatch_ab';
const COOKIE_MAX_AGE = 60 * 60 * 24 * 90;

function parseCookie(cookieHeader, name) {
  if (!cookieHeader) return null;
  const parts = cookieHeader.split(';');
  for (const part of parts) {
    const [rawKey, ...rest] = part.trim().split('=');
    if (rawKey === name) return rest.join('=') || null;
  }
  return null;
}

function pickVariant(request) {
  const existing = parseCookie(request.headers.get('Cookie') || '', AB_COOKIE);
  if (existing === 'a' || existing === '9eur') return { variant: existing, isNew: false };
  const bytes = new Uint8Array(1);
  crypto.getRandomValues(bytes);
  return { variant: bytes[0] < 128 ? 'a' : '9eur', isNew: true };
}

function appendSearch(targetPath, search) {
  return targetPath + (search || '');
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (request.method === 'GET' && url.pathname.replace(/\/+$/, '') === '/start') {
      const { variant } = pickVariant(request);
      const target = variant === '9eur' ? '/9eur/' : '/';
      const redirectUrl = new URL(appendSearch(target, url.search), url.origin);
      const headers = new Headers({ Location: redirectUrl.toString() });
      headers.append('Set-Cookie', `${AB_COOKIE}=${variant}; Max-Age=${COOKIE_MAX_AGE}; Path=/; Secure; SameSite=Lax`);
      headers.append('Cache-Control', 'no-store');
      return new Response(null, { status: 302, headers });
    }

    return env.ASSETS.fetch(request);
  }
};
