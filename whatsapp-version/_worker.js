const COOKIE_MAX_AGE = 60 * 60 * 24 * 180;

function appendSearch(path, search) {
  return `${path}${search || ''}`;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const normalizedPath = url.pathname.replace(/\/+$/, '') || '/';

    if (request.method === 'GET' && (
      normalizedPath === '/start' ||
      normalizedPath === '/9euro' ||
      normalizedPath === '/9eur' ||
      normalizedPath === '/30days'
    )) {
      const redirectUrl = new URL(appendSearch('/', url.search), url.origin);
      const headers = new Headers({ Location: redirectUrl.toString() });
      headers.append('Set-Cookie', `clawhatch_ab=9eur; Max-Age=${COOKIE_MAX_AGE}; Path=/; Secure; SameSite=Lax`);
      headers.append('Cache-Control', 'no-store');
      return new Response(null, { status: 302, headers });
    }

    return env.ASSETS.fetch(request);
  }
};
