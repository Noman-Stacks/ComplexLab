/**
 * ComplexLab - Interactive Practice & Exercises Controller
 */

class PracticeApp {
  constructor() {
    this.currentTopic = 'all';
    this.currentDifficulty = 'beginner';
    this.currentQuestion = null;
    this.selectedOption = null;

    // Score stats
    this.stats = {
      correct: 0,
      total: 0,
      streak: 0,
      bestStreak: 0
    };

    this.init();
  }

  init() {
    this.loadStats();
    this.bindEvents();
    this.fetchNewQuestion();
  }

  loadStats() {
    try {
      const saved = localStorage.getItem('complexlab_practice_stats');
      if (saved) {
        this.stats = JSON.parse(saved);
        this.updateStatsUI();
      }
    } catch (e) {
      console.error('Failed to load practice stats:', e);
    }
  }

  saveStats() {
    try {
      localStorage.setItem('complexlab_practice_stats', JSON.stringify(this.stats));
    } catch (e) {
      console.error('Failed to save practice stats:', e);
    }
  }

  updateStatsUI() {
    const elStreak = document.getElementById('statStreak');
    const elCorrect = document.getElementById('statCorrect');
    const elTotal = document.getElementById('statTotal');
    const elAccuracy = document.getElementById('statAccuracy');

    if (elStreak) elStreak.textContent = this.stats.streak;
    if (elCorrect) elCorrect.textContent = this.stats.correct;
    if (elTotal) elTotal.textContent = this.stats.total;
    if (elAccuracy) {
      const pct = this.stats.total > 0 ? Math.round((this.stats.correct / this.stats.total) * 100) : 0;
      elAccuracy.textContent = `${pct}%`;
    }
  }

  bindEvents() {
    // Topic pills
    document.querySelectorAll('.topic-pill').forEach(pill => {
      pill.addEventListener('click', (e) => {
        document.querySelectorAll('.topic-pill').forEach(p => p.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.currentTopic = e.currentTarget.dataset.topic;
        this.fetchNewQuestion();
      });
    });

    // Difficulty buttons
    document.querySelectorAll('.diff-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.diff-btn').forEach(b => b.classList.remove('active'));
        e.currentTarget.classList.add('active');
        this.currentDifficulty = e.currentTarget.dataset.diff;
        this.fetchNewQuestion();
      });
    });

    // Action buttons
    const btnCheck = document.getElementById('btnCheckAnswer');
    if (btnCheck) btnCheck.addEventListener('click', () => this.checkAnswer());

    const btnNext = document.getElementById('btnNextQuestion');
    if (btnNext) btnNext.addEventListener('click', () => this.fetchNewQuestion());

    const btnHint = document.getElementById('btnShowHint');
    if (btnHint) btnHint.addEventListener('click', () => this.toggleHint());

    const btnReveal = document.getElementById('btnRevealSolution');
    if (btnReveal) btnReveal.addEventListener('click', () => this.toggleSolution());

    const btnResetStats = document.getElementById('btnResetStats');
    if (btnResetStats) {
      btnResetStats.addEventListener('click', () => {
        if (confirm('Reset your practice score statistics?')) {
          this.stats = { correct: 0, total: 0, streak: 0, bestStreak: 0 };
          this.saveStats();
          this.updateStatsUI();
          if (window.showToast) window.showToast('Practice stats reset.', 'info');
        }
      });
    }

    // Enter key submit in practice free input
    const freeInp = document.getElementById('practiceAnswerInput');
    if (freeInp) {
      freeInp.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          this.checkAnswer();
        }
      });
    }
  }

  async fetchNewQuestion() {
    this.selectedOption = null;
    const card = document.getElementById('questionCard');
    const feedbackBox = document.getElementById('practiceFeedback');
    const hintBox = document.getElementById('practiceHint');
    const solBox = document.getElementById('practiceSolution');

    if (feedbackBox) feedbackBox.style.display = 'none';
    if (hintBox) hintBox.style.display = 'none';
    if (solBox) solBox.style.display = 'none';

    try {
      const resp = await fetch('/api/practice/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: this.currentTopic,
          difficulty: this.currentDifficulty
        })
      });

      const data = await resp.json();
      if (!data.success) throw new Error(data.error || 'Failed to generate question.');

      this.currentQuestion = data.question;
      this.renderQuestion(this.currentQuestion);

    } catch (e) {
      console.error('Error fetching practice question:', e);
      if (window.showToast) window.showToast('Could not load question. Please try again.', 'error');
    }
  }

  renderQuestion(q) {
    const qTextEl = document.getElementById('questionText');
    const qBadge = document.getElementById('questionBadge');
    const mcContainer = document.getElementById('mcContainer');
    const freeContainer = document.getElementById('freeInputContainer');
    const inputEl = document.getElementById('practiceAnswerInput');

    if (qBadge) {
      qBadge.textContent = `${q.topic.replace(/_/g, ' ')} • ${q.difficulty}`;
    }

    if (qTextEl) {
      qTextEl.innerHTML = q.question;
    }

    if (q.type === 'multiple_choice') {
      if (mcContainer) mcContainer.style.display = 'grid';
      if (freeContainer) freeContainer.style.display = 'none';

      mcContainer.innerHTML = q.options.map(opt => `
        <button type="button" class="option-btn" data-val="${opt}">
          $${opt}$
        </button>
      `).join('');

      mcContainer.querySelectorAll('.option-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
          mcContainer.querySelectorAll('.option-btn').forEach(b => b.classList.remove('selected'));
          e.currentTarget.classList.add('selected');
          this.selectedOption = e.currentTarget.dataset.val;
        });
      });
    } else {
      if (mcContainer) mcContainer.style.display = 'none';
      if (freeContainer) freeContainer.style.display = 'flex';
      if (inputEl) {
        inputEl.value = '';
        inputEl.focus();
      }
    }

    // Typeset MathJax
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([qTextEl, mcContainer]).catch(err => console.error(err));
    }
  }

  async checkAnswer() {
    if (!this.currentQuestion) return;

    let answer = '';
    if (this.currentQuestion.type === 'multiple_choice') {
      if (!this.selectedOption) {
        if (window.showToast) window.showToast('Please select an option first.', 'info');
        return;
      }
      answer = this.selectedOption;
    } else {
      const inp = document.getElementById('practiceAnswerInput');
      answer = inp ? inp.value.trim() : '';
      if (!answer) {
        if (window.showToast) window.showToast('Please enter an answer.', 'info');
        return;
      }
    }

    try {
      const resp = await fetch('/api/practice/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: this.currentQuestion,
          answer: answer
        })
      });

      const data = await resp.json();
      if (!data.success) throw new Error(data.error || 'Failed to check answer.');

      const res = data.result;

      // Update Stats
      this.stats.total += 1;
      if (res.correct) {
        this.stats.correct += 1;
        this.stats.streak += 1;
        this.stats.bestStreak = Math.max(this.stats.bestStreak, this.stats.streak);
      } else {
        this.stats.streak = 0;
      }
      this.saveStats();
      this.updateStatsUI();

      // Show Feedback
      const feedbackBox = document.getElementById('practiceFeedback');
      if (feedbackBox) {
        feedbackBox.style.display = 'block';
        feedbackBox.className = `feedback-box ${res.correct ? 'correct' : 'incorrect'}`;
        feedbackBox.innerHTML = `
          <div style="font-weight: 700; margin-bottom: 0.25rem;">
            ${res.correct ? '🎉 Correct!' : '❌ Not Quite'}
          </div>
          <div>${res.feedback}</div>
        `;
      }

      // If incorrect, automatically show solution reveal button
      if (!res.correct) {
        this.revealSolution();
      }

    } catch (e) {
      console.error('Error verifying answer:', e);
      if (window.showToast) window.showToast('Verification failed. Try again.', 'error');
    }
  }

  toggleHint() {
    const hintBox = document.getElementById('practiceHint');
    if (!hintBox || !this.currentQuestion) return;

    const isVisible = hintBox.style.display === 'block';
    hintBox.style.display = isVisible ? 'none' : 'block';
    hintBox.innerHTML = `
      <strong>💡 Hint:</strong> ${this.currentQuestion.hint || 'Review the relevant formula in the Learning Center.'}
    `;

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([hintBox]).catch(err => console.error(err));
    }
  }

  toggleSolution() {
    const solBox = document.getElementById('practiceSolution');
    if (!solBox || !this.currentQuestion) return;

    if (solBox.style.display === 'block') {
      solBox.style.display = 'none';
    } else {
      this.revealSolution();
    }
  }

  revealSolution() {
    const solBox = document.getElementById('practiceSolution');
    if (!solBox || !this.currentQuestion) return;

    const q = this.currentQuestion;
    const steps = q.steps;
    const finalAns = q.correct_answer || '';

    let contentHtml = '';

    if (steps && steps.length > 0) {
      contentHtml = `
        <div class="practice-steps-wrapper">
          <div class="practice-steps-header">
            <span class="practice-steps-title">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Complete Step-by-Step Solution
            </span>
            <span class="practice-steps-count">${steps.length} Steps</span>
          </div>

          <div class="practice-steps-list">
            ${steps.map((s, idx) => `
              <div class="practice-step-card">
                <div class="practice-step-top">
                  <span class="practice-step-num">Step ${s.step || (idx + 1)}</span>
                  <span class="practice-step-name">${s.title}</span>
                </div>
                ${s.description ? `<p class="practice-step-text">${s.description}</p>` : ''}
                ${s.latex ? `<div class="practice-step-math">$$${s.latex}$$</div>` : ''}
              </div>
            `).join('')}
          </div>

          <div class="practice-final-answer-card">
            <span class="final-badge">Final Answer</span>
            <div class="final-answer-text">$${finalAns}$</div>
          </div>
        </div>
      `;
    } else {
      contentHtml = `
        <div class="practice-steps-wrapper">
          <div class="practice-steps-header">
            <span class="practice-steps-title">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
              Complete Step-by-Step Solution
            </span>
          </div>
          <div style="white-space: pre-line; padding: 0.75rem 0; font-size: 0.95rem; line-height: 1.6;">
            ${q.solution}
          </div>
          <div class="practice-final-answer-card">
            <span class="final-badge">Final Answer</span>
            <div class="final-answer-text">$${finalAns}$</div>
          </div>
        </div>
      `;
    }

    solBox.style.display = 'block';
    solBox.innerHTML = contentHtml;

    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise([solBox]).catch(err => console.error(err));
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('practiceAppContainer')) {
    window.practiceApp = new PracticeApp();
  }
});
