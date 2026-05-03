/* ================================================================
   RDMS CHATBOT (mockup, presentation only)
   - Knowledge: parsed from .faq__item entries already in the DOM.
   - No backend, no LLM, no network calls.
   - Free-text input → simple keyword scoring against question +
     answer text → returns best match or graceful fallback.
   - Quick-reply chips for popular questions and audience routing.
   ================================================================ */
(function () {
  'use strict';

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  ready(function () {
    var launcher = document.getElementById('chatbotLauncher');
    var panel    = document.getElementById('chatbotPanel');
    var body     = document.getElementById('chatbotBody');
    var form     = document.getElementById('chatbotForm');
    var input    = document.getElementById('chatbotInput');
    var closeBtn = document.getElementById('chatbotClose');

    if (!launcher || !panel || !body || !form || !input) return;

    /* Stop words: ignore common English to reduce match noise.
       MUST be defined before the FAQ parsing loop calls bagOfWords. */
    var STOP = new Set([
      'a','an','the','is','are','was','were','be','been','being','of','to','in',
      'on','at','for','with','by','as','and','or','if','it','its','this','that',
      'these','those','do','does','did','can','i','you','we','my','our','your',
      'me','us','they','them','their','what','when','where','who','whom','how',
      'why','which','about','from','into','out','up','down','so','than','then',
      'have','has','had','will','would','could','should','may','might','must',
      'not','no','any','some','all','more','most','other','such','just','only',
      'rdms','dental','health'  /* these terms appear too broadly */
    ]);

    function bagOfWords(text) {
      var words = text.toLowerCase().match(/[a-z][a-z'-]+/g) || [];
      var out = {};
      words.forEach(function (w) {
        if (w.length < 3) return;
        if (STOP.has(w)) return;
        out[w] = (out[w] || 0) + 1;
      });
      return out;
    }

    /* --------- Knowledge base: parse the FAQ entries ------------ */
    var knowledge = [];
    var faqItems = document.querySelectorAll('.faq__item');
    faqItems.forEach(function (item) {
      var qEl = item.querySelector('.faq__question');
      var aEl = item.querySelector('.faq__answer');
      if (!qEl || !aEl) return;
      knowledge.push({
        question: qEl.textContent.trim(),
        answer: aEl.innerHTML.trim(),
        bag: bagOfWords(qEl.textContent + ' ' + aEl.textContent)
      });
    });

    function findAnswer(query) {
      var qBag = bagOfWords(query);
      var qKeys = Object.keys(qBag);
      if (!qKeys.length) return null;
      var best = null, bestScore = 0;
      knowledge.forEach(function (item) {
        var score = 0;
        qKeys.forEach(function (k) {
          if (item.bag[k]) score += qBag[k] * item.bag[k];
        });
        /* Bonus: exact-question substring match. */
        if (item.question.toLowerCase().indexOf(query.toLowerCase().trim()) !== -1) {
          score += 50;
        }
        if (score > bestScore) {
          bestScore = score;
          best = item;
        }
      });
      /* Threshold to avoid weak matches. */
      return bestScore >= 1 ? best : null;
    }

    /* --------- Curated suggestion chips -------------------------- */
    /* Hand-picked common opening questions, mapped to the parsed
       knowledge entries by question-text match. */
    var POPULAR_QS = [
      'What is RDMS?',
      'Are RDMS services free?',
      'How can I support RDMS as a donor?',
      'Who can become a member of RDMS?',
      'How can I contact RDMS?',
      'What should I do if I have a dental emergency?'
    ];

    var AUDIENCE_QS = [
      { label: 'I\'m a donor', q: 'How can I support RDMS as a donor?' },
      { label: 'I\'m a community member', q: 'How do I access RDMS’s dental services?' },
      { label: 'I\'m a dental professional', q: 'Who can become a member of RDMS?' },
      { label: 'Just curious', q: 'What is RDMS?' }
    ];

    /* --------- DOM helpers --------------------------------------- */
    function el(tag, className, html) {
      var n = document.createElement(tag);
      if (className) n.className = className;
      if (html != null) n.innerHTML = html;
      return n;
    }

    function scrollToBottom() {
      body.scrollTop = body.scrollHeight;
    }

    function addUserMsg(text) {
      var msg = el('div', 'chatbot-msg chatbot-msg--user');
      msg.appendChild(el('div', 'chatbot-msg__bubble', escapeHtml(text)));
      body.appendChild(msg);
      scrollToBottom();
    }

    function addBotMsg(html) {
      var msg = el('div', 'chatbot-msg chatbot-msg--bot');
      msg.appendChild(el('div', 'chatbot-msg__bubble', html));
      body.appendChild(msg);
      scrollToBottom();
      return msg;
    }

    function addTypingIndicator() {
      var msg = el('div', 'chatbot-msg chatbot-msg--bot');
      var bubble = el('div', 'chatbot-msg__bubble');
      bubble.style.padding = '0';
      var typing = el('div', 'chatbot-typing');
      typing.appendChild(el('span'));
      typing.appendChild(el('span'));
      typing.appendChild(el('span'));
      bubble.appendChild(typing);
      msg.appendChild(bubble);
      body.appendChild(msg);
      scrollToBottom();
      return msg;
    }

    function addSuggestions(items) {
      var wrap = el('div', 'chatbot-suggestions');
      items.forEach(function (item) {
        var label = typeof item === 'string' ? item : item.label;
        var query = typeof item === 'string' ? item : item.q;
        var chip = el('button', 'chatbot-chip');
        chip.type = 'button';
        chip.textContent = label;
        chip.addEventListener('click', function () {
          handleQuery(query, label);
        });
        wrap.appendChild(chip);
      });
      body.appendChild(wrap);
      scrollToBottom();
    }

    function escapeHtml(s) {
      return String(s)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    /* --------- Conversation flow --------------------------------- */
    var conversationStarted = false;

    function startConversation() {
      if (conversationStarted) return;
      conversationStarted = true;
      addBotMsg(
        '<strong>Murakaza neza.</strong> I\'m the RDMS demo assistant. I can answer questions about programs, services, partnerships, and oral health basics, drawing from our published FAQ.'
      );
      setTimeout(function () {
        addBotMsg('Who are you, or what would you like to ask?');
        addSuggestions(AUDIENCE_QS);
      }, 600);
      setTimeout(function () {
        addBotMsg('Or pick a popular question:');
        addSuggestions(POPULAR_QS);
      }, 1400);
    }

    function handleQuery(query, displayText) {
      var q = (query || '').trim();
      if (!q) return;
      addUserMsg(displayText || q);
      input.value = '';

      var typing = addTypingIndicator();
      var match = findAnswer(q);

      var delay = 600 + Math.min(900, q.length * 20);
      setTimeout(function () {
        typing.remove();
        if (match) {
          addBotMsg(match.answer);
          /* Suggest 3 related questions (random sample, excluding match) */
          var others = knowledge
            .filter(function (k) { return k !== match; })
            .sort(function () { return Math.random() - 0.5; })
            .slice(0, 3)
            .map(function (k) { return k.question; });
          if (others.length) {
            setTimeout(function () {
              addBotMsg('Related questions:');
              addSuggestions(others);
            }, 400);
          }
        } else {
          addBotMsg(
            'I don\'t have an answer for that in our published FAQ. Try asking about programs, services, partnership, membership, or oral health basics. Or <a href="#contact">write to us directly</a> and the team will reply.'
          );
          /* Surface popular questions to recover. */
          setTimeout(function () {
            addSuggestions(POPULAR_QS.slice(0, 4));
          }, 300);
        }
      }, delay);
    }

    /* --------- Open / close ------------------------------------- */
    function openPanel() {
      panel.classList.add('is-open');
      panel.setAttribute('aria-hidden', 'false');
      launcher.classList.add('is-open');
      launcher.setAttribute('aria-expanded', 'true');
      startConversation();
      setTimeout(function () { input.focus(); }, 320);
    }

    function closePanel() {
      panel.classList.remove('is-open');
      panel.setAttribute('aria-hidden', 'true');
      launcher.classList.remove('is-open');
      launcher.setAttribute('aria-expanded', 'false');
      launcher.focus();
    }

    /* --------- Wire events --------------------------------------- */
    launcher.addEventListener('click', openPanel);
    if (closeBtn) closeBtn.addEventListener('click', closePanel);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) {
        closePanel();
      }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = input.value.trim();
      if (q) handleQuery(q);
    });
  });
})();
