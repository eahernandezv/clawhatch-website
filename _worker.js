const PASS_THROUGH_PREFIXES = [
  '/privacy',
  '/terms',
  '/data-deletion',
  '/success',
  '/c/success',
  '/favicon.svg',
  '/robots.txt',
  '/sitemap.xml'
];

function shouldPassThrough(pathname) {
  const normalized = pathname.replace(/\/+$/, '') || '/';
  return PASS_THROUGH_PREFIXES.some((prefix) => normalized === prefix || normalized.startsWith(`${prefix}/`));
}

export default {
  async fetch(request, env) {
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return env.ASSETS.fetch(request);
    }

    const url = new URL(request.url);
    if (shouldPassThrough(url.pathname)) {
      return env.ASSETS.fetch(request);
    }

    const closureUrl = new URL('/index.html', url.origin);
    const closureRequest = new Request(closureUrl.toString(), request);
    const response = await env.ASSETS.fetch(closureRequest);
    const headers = new Headers(response.headers);
    headers.set('Cache-Control', 'no-store, max-age=0');
    return new Response(response.body, { status: response.status, statusText: response.statusText, headers });
  }
};
