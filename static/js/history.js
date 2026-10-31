/**
 * ComplexLab - Calculation History Manager
 * Uses localStorage to persist recent calculations without user tracking.
 */

class HistoryManager {
  constructor(listElementId) {
    this.storageKey = 'complexlab_history_v1';
    this.maxItems = 30;
    this.listEl = document.getElementById(listElementId);
    this.init();
  }

  init() {
    this.render();
  }

  getHistory() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : [];
    } catch (e) {
      console.error('Failed to read calculation history from localStorage', e);
      return [];
    }
  }

  saveHistory(list) {
    try {
      localStorage.setItem(this.storageKey, JSON.stringify(list.slice(0, this.maxItems)));
    } catch (e) {
      console.error('Failed to write calculation history to localStorage', e);
    }
  }

  addEntry(entry) {
    const list = this.getHistory();
    const item = {
      id: Date.now().toString(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      operation: entry.operation,
      z1: entry.z1,
      z2: entry.z2,
      result: entry.result,
      latex: entry.latex || '',
      steps: entry.steps || []
    };
    list.unshift(item);
    this.saveHistory(list);
    this.render();
  }

  deleteEntry(id) {
    let list = this.getHistory();
    list = list.filter(item => item.id !== id);
    this.saveHistory(list);
    this.render();
    if (window.showToast) window.showToast('Calculation removed from history.', 'info');
  }

  clearHistory() {
    if (confirm('Are you sure you want to clear your calculation history?')) {
      localStorage.removeItem(this.storageKey);
      this.render();
      if (window.showToast) window.showToast('History cleared.', 'info');
    }
  }

  render() {
    if (!this.listEl) return;
    const list = this.getHistory();

    if (list.length === 0) {
      this.listEl.innerHTML = `
        <div style="text-align: center; padding: 2rem 1rem; color: var(--text-muted); font-size: 0.875rem;">
          No calculations yet. Perform a calculation above to see your history.
        </div>`;
      return;
    }

    this.listEl.innerHTML = list.map(item => {
      let inputsDesc = item.z1 ? item.z1 : '';
      if (item.z2) inputsDesc += ` & ${item.z2}`;

      return `
        <div class="history-item" data-id="${item.id}">
          <div class="history-info">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <span class="history-op">${this.formatOpName(item.operation)}</span>
              <span style="font-size: 0.75rem; color: var(--text-muted);">${item.timestamp}</span>
            </div>
            <div class="history-expr">${inputsDesc}</div>
            <div class="history-res">= ${item.result}</div>
          </div>
          <div class="history-actions">
            <button class="btn btn-sm btn-outline" title="Load into Calculator" onclick="historyManager.loadEntry('${item.id}')">
              <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </button>
            <button class="btn btn-sm btn-outline" title="Copy Result" onclick="historyManager.copyResult('${item.id}')">
              <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
            </button>
            <button class="btn btn-sm btn-outline" style="color: var(--accent-danger);" title="Delete" onclick="historyManager.deleteEntry('${item.id}')">
              <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            </button>
          </div>
        </div>`;
    }).join('');
  }

  loadEntry(id) {
    const list = this.getHistory();
    const item = list.find(it => it.id === id);
    if (!item) return;

    if (window.calculatorApp && window.calculatorApp.loadFromHistory) {
      window.calculatorApp.loadFromHistory(item);
    }
  }

  copyResult(id) {
    const list = this.getHistory();
    const item = list.find(it => it.id === id);
    if (item && window.copyToClipboard) {
      window.copyToClipboard(item.result);
    }
  }

  exportHistory() {
    const list = this.getHistory();
    if (list.length === 0) {
      alert('History is empty.');
      return;
    }

    let text = `ComplexLab Calculation History Export\nGenerated: ${new Date().toLocaleString()}\n` + '='.repeat(50) + '\n\n';
    list.forEach((item, index) => {
      text += `[${index + 1}] Operation: ${this.formatOpName(item.operation)}\n`;
      text += `Time: ${item.timestamp}\n`;
      text += `Input: z1 = ${item.z1 || 'N/A'}`;
      if (item.z2) text += `, z2 = ${item.z2}`;
      text += `\nResult: ${item.result}\n`;
      if (item.steps && item.steps.length > 0) {
        text += 'Steps:\n';
        item.steps.forEach(s => {
          text += `  - ${s.title}: ${s.latex}\n`;
        });
      }
      text += '\n' + '-'.repeat(40) + '\n\n';
    });

    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ComplexLab_History_${new Date().toISOString().slice(0, 10)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  formatOpName(op) {
    return op.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  }
}

window.HistoryManager = HistoryManager;
