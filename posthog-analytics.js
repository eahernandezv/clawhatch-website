/**
 * PostHog Analytics for ClawHatch
 * --------------------------------
 * Privacy-conscious event tracking for landing page optimization.
 * 
 * Events tracked:
 *   - $pageview (automatic via PostHog)
 *   - $pageleave (automatic via PostHog)
 *   - scroll_depth_25/50/75/100
 *   - section_viewed (pricing, use-cases, specs, reviews, faq, why-us)
 *   - cta_clicked (hero, sticky, banner, header, pricing, modal)
 *   - checkout_started (with tier, variant, selected_credit)
 *   - pricing_modal_opened / pricing_modal_closed
 *   - faq_opened
 *   - engagement_time (10s, 30s, 60s, 120s)
 *   - page_exit (deepest_section, time_on_page_s)
 *   - hero_cta_visible
 *   - outbound_click
 *   - waitlist_submitted
 * 
 * Person super-properties (set once):
 *   - variant, landing_path, referrer, utm_source/medium/campaign/content/term
 */
(function () {
  'use strict';

  // ── BOOT ──
  // analytics-config.js sets window.__ANALYTICS but defer ordering can race on CDNs.
  // We try immediately, then retry at DOMContentLoaded if needed.
  function getKey() {
    var cfg = window.__ANALYTICS || {};
    return cfg.posthog_key || '';
  }
  function getHost() {
    var cfg = window.__ANALYTICS || {};
    return cfg.posthog_host || 'https://us.i.posthog.com';
  }

  function tryBoot() {
    var key = getKey();
    if (!key || key.indexOf('REPLACE') !== -1) return false;
    run(key, getHost());
    return true;
  }

  if (!tryBoot()) {
    // Retry once DOM is ready (analytics-config.js will definitely have executed)
    var retried = false;
    function retryBoot() {
      if (retried) return;
      retried = true;
      if (!tryBoot()) {
        console.warn('[PostHog] API key not configured. Set window.__ANALYTICS.posthog_key in analytics-config.js');
      }
    }
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', retryBoot);
    } else {
      // Already loaded — truly missing
      console.warn('[PostHog] API key not configured. Set window.__ANALYTICS.posthog_key in analytics-config.js');
    }
    return;
  }

  function run(POSTHOG_API_KEY, POSTHOG_HOST) {

  // ── LOAD POSTHOG SNIPPET ──
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  posthog.init(POSTHOG_API_KEY, {
    api_host: POSTHOG_HOST,
    person_profiles: 'identified_only',
    capture_pageview: true,
    capture_pageleave: true,
    autocapture: false,
    disable_session_recording: true,
    persistence: 'localStorage+cookie',
    cross_subdomain_cookie: false,
    secure_cookie: true,
    respect_dnt: true,
  });

  var pageLoadTime = Date.now();

  // ── ATTRIBUTION ──
  var params = new URLSearchParams(window.location.search);
  var attribution = {};
  var variant = params.get('v');
  if (variant) attribution.variant = variant;
  attribution.landing_path = window.location.pathname;
  if (document.referrer) {
    try { if (new URL(document.referrer).hostname !== window.location.hostname) attribution.referrer = document.referrer; } catch(_){}
  }
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
    var v = params.get(k);
    if (v) attribution[k] = v;
  });
  if (Object.keys(attribution).length) {
    posthog.register_once(attribution);
  }

  // ── SCROLL DEPTH ──
  var scrollFired = {};
  function checkScroll() {
    var total = document.documentElement.scrollHeight - window.innerHeight;
    if (total <= 0) return;
    var scrollPct = Math.round((window.scrollY / total) * 100);
    [25, 50, 75, 100].forEach(function (m) {
      if (scrollPct >= m && !scrollFired[m]) {
        scrollFired[m] = true;
        posthog.capture('scroll_depth_' + m);
      }
    });
  }
  window.addEventListener('scroll', throttle(checkScroll, 300), { passive: true });

  // ── SECTION VISIBILITY ──
  var sectionsFired = {};
  var sectionIds = ['pricing', 'use-cases', 'specs', 'reviews', 'faq', 'why-us'];
  if (typeof IntersectionObserver !== 'undefined') {
    var sectionObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && !sectionsFired[entry.target.id]) {
          sectionsFired[entry.target.id] = true;
          posthog.capture('section_viewed', { section: entry.target.id });
        }
      });
    }, { threshold: 0.3 });
    sectionIds.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) sectionObs.observe(el);
    });
  }

  // ── CTA CLICKS (delegated) ──
  document.addEventListener('click', function (e) {
    var target = e.target.closest('a, button');
    if (!target) return;

    var text = (target.textContent || '').trim().toLowerCase();
    var loc = target.getAttribute('data-cta-location') || 'unknown';
    var ctaTarget = target.getAttribute('data-cta-target') || undefined;
    var ctaLabel = target.getAttribute('data-cta-label') || text.slice(0, 80);

    if (target.hasAttribute('data-cta-location')) {
      return;
    }

    if (target.closest('.hero-cta') || target.closest('.hero')) loc = 'hero';
    else if (target.closest('#sticky-cta-bar')) loc = 'sticky';
    else if (target.closest('.cta-banner')) loc = 'banner';
    else if (target.closest('header')) loc = 'header';
    else if (target.closest('#pricing')) loc = 'pricing';
    else if (target.closest('.modal')) loc = 'modal';

    if (text.indexOf('free trial') !== -1 || text.indexOf('try it free') !== -1 ||
        text.indexOf('start 7-day') !== -1 || text.indexOf('redirecting') !== -1 ||
        text.indexOf('pay with stripe') !== -1) {
      posthog.capture('cta_clicked', { location: loc, target: ctaTarget, label: ctaLabel, text: text.slice(0, 80) });
    }

    // Waitlist
    if (target.type === 'submit' && target.closest('#waitlist-form')) {
      posthog.capture('waitlist_submitted');
    }
  });

  // ── CHECKOUT STARTED (monkey-patch) ──
  function hookCheckout() {
    var orig = window.startCheckout;
    if (typeof orig === 'function' && !orig.__ph) {
      window.startCheckout = function (tier) {
        posthog.capture('checkout_started', {
          tier: tier,
          variant: variant || 'a',
          selected_credit: window.selectedCredit || 'later',
        });
        return orig.apply(this, arguments);
      };
      window.startCheckout.__ph = true;
      return true;
    }
    return false;
  }
  // startCheckout is defined in inline <script> which runs after defer scripts,
  // so hook after DOM is ready.
  if (!hookCheckout()) {
    document.addEventListener('DOMContentLoaded', function () {
      if (!hookCheckout()) setTimeout(hookCheckout, 500);
    });
    window.addEventListener('load', hookCheckout);
  }

  // ── PRICING MODAL OPEN/CLOSE ──
  function watchModal() {
    var modal = document.getElementById('checkout-modal');
    if (!modal) return;
    var wasActive = false;
    new MutationObserver(function () {
      var isActive = modal.classList.contains('active');
      if (isActive && !wasActive) posthog.capture('pricing_modal_opened', { variant: variant || 'a' });
      else if (!isActive && wasActive) posthog.capture('pricing_modal_closed', { variant: variant || 'a' });
      wasActive = isActive;
    }).observe(modal, { attributes: true, attributeFilter: ['class'] });
  }
  if (document.getElementById('checkout-modal')) watchModal();
  else document.addEventListener('DOMContentLoaded', watchModal);

  // ── FAQ OPENED ──
  function hookFaq() {
    document.querySelectorAll('.faq-q').forEach(function (q, i) {
      if (q.__ph_faq) return;
      q.__ph_faq = true;
      q.addEventListener('click', function () {
        var item = q.parentElement;
        if (!item.classList.contains('open')) {
          posthog.capture('faq_opened', {
            question: q.textContent.trim().replace(/\s*[▾▸↓→]\s*$/, '').slice(0, 80),
            index: i,
          });
        }
      });
    });
  }
  hookFaq();
  document.addEventListener('DOMContentLoaded', hookFaq);

  // ── ENGAGEMENT TIME THRESHOLDS ──
  [10, 30, 60, 120].forEach(function (sec) {
    setTimeout(function () {
      if (!document.hidden) {
        posthog.capture('engagement_time', { seconds: sec });
      }
    }, sec * 1000);
  });

  // ── DEEPEST SECTION + PAGE EXIT ──
  var deepestSection = 'none';
  var orderedSections = ['main', 'why-us', 'use-cases', 'specs', 'reviews', 'pricing', 'faq'];
  if (typeof IntersectionObserver !== 'undefined') {
    var depthObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var idx = orderedSections.indexOf(entry.target.id);
          var cur = orderedSections.indexOf(deepestSection);
          if (idx > cur) deepestSection = entry.target.id;
        }
      });
    }, { threshold: 0.2 });
    orderedSections.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) depthObs.observe(el);
    });
  }
  window.addEventListener('beforeunload', function () {
    posthog.capture('page_exit', {
      deepest_section: deepestSection,
      time_on_page_s: Math.round((Date.now() - pageLoadTime) / 1000),
    });
  });

  // ── HERO CTA VISIBILITY ──
  var heroCta = document.querySelector('.hero-cta');
  if (heroCta && typeof IntersectionObserver !== 'undefined') {
    var heroObs = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) {
        posthog.capture('hero_cta_visible');
        heroObs.disconnect();
      }
    }, { threshold: 0.5 });
    heroObs.observe(heroCta);
  }

  // ── OUTBOUND LINK CLICKS ──
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a[href]');
    if (!link) return;
    try {
      var url = new URL(link.href, window.location.origin);
      if (url.hostname !== window.location.hostname && url.protocol.indexOf('http') === 0) {
        posthog.capture('outbound_click', { url: url.href, text: (link.textContent || '').trim().slice(0, 60) });
      }
    } catch (_) {}
  });

  } // end run()

  // ── UTILITY ──
  function throttle(fn, ms) {
    var last = 0;
    return function () {
      var now = Date.now();
      if (now - last >= ms) { last = now; fn(); }
    };
  }
})();
