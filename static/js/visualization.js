/**
 * ComplexLab - Interactive Complex Plane Canvas
 * High-DPI canvas supporting pan, zoom, grid, vectors, angles, roots, and tooltips.
 */

class ComplexPlane {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');
    this.container = this.canvas.parentElement;

    // View State
    this.originX = 0;
    this.originY = 0;
    this.scale = 40; // pixels per mathematical unit
    this.minScale = 8;
    this.maxScale = 300;

    // Interaction State
    this.isDragging = false;
    this.dragStartX = 0;
    this.dragStartY = 0;
    this.mouseMathX = 0;
    this.mouseMathY = 0;

    // Data to plot
    this.elements = {
      z1: null,        // {real, imag, label}
      z2: null,        // {real, imag, label}
      result: null,    // {real, imag, label}
      conjugate: null, // {real, imag, label}
      roots: [],       // array of {real, imag, label, k}
      showVectorAddition: false,
      showArgArc: true
    };

    this.tooltip = document.getElementById('planeTooltip');

    this.init();
  }

  init() {
    this.resize();
    this.centerOrigin();

    // Event listeners
    window.addEventListener('resize', () => {
      this.resize();
      this.draw();
    });

    window.addEventListener('themeChanged', () => {
      this.draw();
    });

    // Mouse Dragging / Panning
    this.canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
    window.addEventListener('mousemove', (e) => this.onMouseMove(e));
    window.addEventListener('mouseup', () => this.onMouseUp());

    // Touch Support
    this.canvas.addEventListener('touchstart', (e) => this.onTouchStart(e), { passive: false });
    this.canvas.addEventListener('touchmove', (e) => this.onTouchMove(e), { passive: false });
    this.canvas.addEventListener('touchend', () => this.onMouseUp());

    // Mouse Wheel Zooming
    this.canvas.addEventListener('wheel', (e) => this.onWheel(e), { passive: false });

    // Initial draw
    this.draw();
  }

  resize() {
    if (!this.container) return;
    const dpr = window.devicePixelRatio || 1;
    const rect = this.container.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height || 480;

    this.canvas.width = width * dpr;
    this.canvas.height = height * dpr;
    this.width = width;
    this.height = height;

    this.ctx.resetTransform();
    this.ctx.scale(dpr, dpr);
  }

  centerOrigin() {
    this.originX = this.width / 2;
    this.originY = this.height / 2;
  }

  resetView(autoScalePoints = true) {
    this.centerOrigin();

    if (autoScalePoints) {
      // Find maximum coordinate among plotted points
      const points = [];
      if (this.elements.z1) points.push(this.elements.z1);
      if (this.elements.z2) points.push(this.elements.z2);
      if (this.elements.result) points.push(this.elements.result);
      if (this.elements.roots && this.elements.roots.length > 0) points.push(...this.elements.roots);

      if (points.length > 0) {
        let maxVal = 0;
        points.forEach(p => {
          maxVal = Math.max(maxVal, Math.abs(p.real), Math.abs(p.imag));
        });
        if (maxVal > 0) {
          const padding = 1.6;
          const minDim = Math.min(this.width, this.height) / 2;
          this.scale = Math.max(this.minScale, Math.min(this.maxScale, minDim / (maxVal * padding)));
        } else {
          this.scale = 40;
        }
      } else {
        this.scale = 40;
      }
    } else {
      this.scale = 40;
    }
    this.draw();
  }

  zoom(factor) {
    const newScale = this.scale * factor;
    if (newScale >= this.minScale && newScale <= this.maxScale) {
      this.scale = newScale;
      this.draw();
    }
  }

  toScreen(real, imag) {
    return {
      x: this.originX + real * this.scale,
      y: this.originY - imag * this.scale
    };
  }

  toMath(screenX, screenY) {
    return {
      real: (screenX - this.originX) / this.scale,
      imag: (this.originY - screenY) / this.scale
    };
  }

  onMouseDown(e) {
    this.isDragging = true;
    const rect = this.canvas.getBoundingClientRect();
    this.dragStartX = e.clientX - rect.left;
    this.dragStartY = e.clientY - rect.top;
    this.canvas.style.cursor = 'grabbing';
  }

  onMouseMove(e) {
    const rect = this.canvas.getBoundingClientRect();
    const curX = e.clientX - rect.left;
    const curY = e.clientY - rect.top;

    if (this.isDragging) {
      const dx = curX - this.dragStartX;
      const dy = curY - this.dragStartY;
      this.originX += dx;
      this.originY += dy;
      this.dragStartX = curX;
      this.dragStartY = curY;
      this.draw();
    } else {
      // Check hover for tooltips
      const mathCoord = this.toMath(curX, curY);
      this.mouseMathX = mathCoord.real;
      this.mouseMathY = mathCoord.imag;
      this.checkHover(curX, curY);
    }
  }

  onMouseUp() {
    this.isDragging = false;
    this.canvas.style.cursor = 'crosshair';
  }

  onTouchStart(e) {
    if (e.touches.length === 1) {
      e.preventDefault();
      this.isDragging = true;
      const rect = this.canvas.getBoundingClientRect();
      this.dragStartX = e.touches[0].clientX - rect.left;
      this.dragStartY = e.touches[0].clientY - rect.top;
    }
  }

  onTouchMove(e) {
    if (this.isDragging && e.touches.length === 1) {
      e.preventDefault();
      const rect = this.canvas.getBoundingClientRect();
      const curX = e.touches[0].clientX - rect.left;
      const curY = e.touches[0].clientY - rect.top;
      const dx = curX - this.dragStartX;
      const dy = curY - this.dragStartY;
      this.originX += dx;
      this.originY += dy;
      this.dragStartX = curX;
      this.dragStartY = curY;
      this.draw();
    }
  }

  onWheel(e) {
    e.preventDefault();
    const rect = this.canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    const mathBefore = this.toMath(mouseX, mouseY);
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.87;
    const newScale = Math.max(this.minScale, Math.min(this.maxScale, this.scale * zoomFactor));

    if (newScale !== this.scale) {
      this.scale = newScale;
      // Re-anchor origin to mouse position
      this.originX = mouseX - mathBefore.real * this.scale;
      this.originY = mouseY + mathBefore.imag * this.scale;
      this.draw();
    }
  }

  checkHover(screenX, screenY) {
    if (!this.tooltip) return;

    const hoverRadius = 10;
    const candidates = [];
    if (this.elements.z1) candidates.push({ ...this.elements.z1, tag: 'z₁' });
    if (this.elements.z2) candidates.push({ ...this.elements.z2, tag: 'z₂' });
    if (this.elements.result) candidates.push({ ...this.elements.result, tag: 'Result' });
    if (this.elements.conjugate) candidates.push({ ...this.elements.conjugate, tag: 'Conjugate' });
    if (this.elements.roots) {
      this.elements.roots.forEach(r => candidates.push({ ...r, tag: `w_${r.k ?? ''}` }));
    }

    let hovered = null;
    for (const c of candidates) {
      const scr = this.toScreen(c.real, c.imag);
      const dist = Math.hypot(scr.x - screenX, scr.y - screenY);
      if (dist <= hoverRadius) {
        hovered = c;
        break;
      }
    }

    if (hovered) {
      const mod = Math.hypot(hovered.real, hovered.imag).toFixed(3);
      let argDeg = (Math.atan2(hovered.imag, hovered.real) * 180 / Math.PI).toFixed(1);
      const imagSign = hovered.imag >= 0 ? '+' : '-';
      const cStr = `${hovered.real.toFixed(2)} ${imagSign} ${Math.abs(hovered.imag).toFixed(2)}i`;

      this.tooltip.innerHTML = `<strong>${hovered.tag}</strong>: ${cStr}<br><span style="color:#94a3b8">|z| = ${mod}, θ = ${argDeg}°</span>`;
      this.tooltip.style.left = `${screenX + 14}px`;
      this.tooltip.style.top = `${screenY - 14}px`;
      this.tooltip.style.display = 'block';
    } else {
      this.tooltip.style.display = 'none';
    }
  }

  draw() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const bgCol = isDark ? '#0b1120' : '#ffffff';
    const gridCol = isDark ? '#1e293b' : '#f1f5f9';
    const axisCol = isDark ? '#64748b' : '#94a3b8';
    const textCol = isDark ? '#94a3b8' : '#64748b';

    // Clear canvas
    ctx.fillStyle = bgCol;
    ctx.fillRect(0, 0, w, h);

    // Dynamic grid step
    let step = 1;
    if (this.scale < 20) step = 5;
    if (this.scale < 10) step = 10;
    if (this.scale > 80) step = 0.5;
    if (this.scale > 150) step = 0.25;

    // Draw Grid
    ctx.lineWidth = 1;
    ctx.strokeStyle = gridCol;

    const startMath = this.toMath(0, h);
    const endMath = this.toMath(w, 0);

    const firstGridX = Math.floor(startMath.real / step) * step;
    const lastGridX = Math.ceil(endMath.real / step) * step;
    const firstGridY = Math.floor(startMath.imag / step) * step;
    const lastGridY = Math.ceil(endMath.imag / step) * step;

    ctx.beginPath();
    for (let r = firstGridX; r <= lastGridX; r += step) {
      const scr = this.toScreen(r, 0);
      ctx.moveTo(scr.x, 0);
      ctx.lineTo(scr.x, h);
    }
    for (let i = firstGridY; i <= lastGridY; i += step) {
      const scr = this.toScreen(0, i);
      ctx.moveTo(0, scr.y);
      ctx.lineTo(w, scr.y);
    }
    ctx.stroke();

    // Draw Main Axes
    ctx.lineWidth = 2;
    ctx.strokeStyle = axisCol;
    ctx.beginPath();
    // Real Axis
    ctx.moveTo(0, this.originY);
    ctx.lineTo(w, this.originY);
    // Imag Axis
    ctx.moveTo(this.originX, 0);
    ctx.lineTo(this.originX, h);
    ctx.stroke();

    // Axis Labels and numbers
    ctx.font = '11px JetBrains Mono, monospace';
    ctx.fillStyle = textCol;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';

    // X axis ticks
    for (let r = firstGridX; r <= lastGridX; r += step) {
      if (Math.abs(r) < 1e-6) continue;
      const scr = this.toScreen(r, 0);
      if (scr.x > 20 && scr.x < w - 20) {
        ctx.fillText(Number(r.toFixed(2)), scr.x, Math.min(Math.max(this.originY + 6, 8), h - 22));
      }
    }

    // Y axis ticks
    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    for (let i = firstGridY; i <= lastGridY; i += step) {
      if (Math.abs(i) < 1e-6) continue;
      const scr = this.toScreen(0, i);
      if (scr.y > 20 && scr.y < h - 20) {
        ctx.fillText(`${Number(i.toFixed(2))}i`, Math.min(Math.max(this.originX - 8, 30), w - 8), scr.y);
      }
    }

    // Origin '0'
    ctx.fillText('0', this.originX - 6, this.originY + 6);

    // Axis Header Labels
    ctx.font = 'bold 12px Inter, sans-serif';
    ctx.fillStyle = axisCol;
    ctx.textAlign = 'right';
    ctx.fillText('Re (Real)', w - 12, this.originY - 14);
    ctx.textAlign = 'left';
    ctx.fillText('Im (Imaginary)', this.originX + 10, 14);

    // Draw N-th roots circle and polygon if roots present
    if (this.elements.roots && this.elements.roots.length > 1) {
      this.drawRootsPolygon(ctx, isDark);
    }

    // Draw Conjugate reflection line if present
    if (this.elements.conjugate && this.elements.z1) {
      this.drawConjugateReflection(ctx);
    }

    // Draw Vectors
    if (this.elements.z2) {
      this.drawVector(this.elements.z2.real, this.elements.z2.imag, '#ec4899', 'z₂');
    }
    if (this.elements.z1) {
      this.drawVector(this.elements.z1.real, this.elements.z1.imag, '#3b82f6', 'z₁');
      if (this.elements.showArgArc) {
        this.drawAngleArc(this.elements.z1.real, this.elements.z1.imag, '#3b82f6', 'θ₁');
      }
    }
    if (this.elements.result) {
      this.drawVector(this.elements.result.real, this.elements.result.imag, '#10b981', 'Result');
    }
  }

  drawVector(real, imag, color, label) {
    if (Math.abs(real) < 1e-9 && Math.abs(imag) < 1e-9) {
      // Draw origin point
      const scr = this.toScreen(0, 0);
      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      this.ctx.arc(scr.x, scr.y, 5, 0, Math.PI * 2);
      this.ctx.fill();
      return;
    }

    const scr = this.toScreen(real, imag);
    const origin = { x: this.originX, y: this.originY };
    const ctx = this.ctx;

    // Dashed projections to axes
    ctx.save();
    ctx.strokeStyle = color;
    ctx.globalAlpha = 0.35;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(scr.x, scr.y);
    ctx.lineTo(scr.x, origin.y);
    ctx.moveTo(scr.x, scr.y);
    ctx.lineTo(origin.x, scr.y);
    ctx.stroke();
    ctx.restore();

    // Main Vector Line
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(origin.x, origin.y);
    ctx.lineTo(scr.x, scr.y);
    ctx.stroke();

    // Arrowhead
    const angle = Math.atan2(scr.y - origin.y, scr.x - origin.x);
    const arrowLen = 10;
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(scr.x, scr.y);
    ctx.lineTo(scr.x - arrowLen * Math.cos(angle - Math.PI / 6), scr.y - arrowLen * Math.sin(angle - Math.PI / 6));
    ctx.lineTo(scr.x - arrowLen * Math.cos(angle + Math.PI / 6), scr.y - arrowLen * Math.sin(angle + Math.PI / 6));
    ctx.closePath();
    ctx.fill();

    // Point
    ctx.beginPath();
    ctx.arc(scr.x, scr.y, 4.5, 0, Math.PI * 2);
    ctx.fill();

    // Label
    ctx.font = 'bold 12px Inter, sans-serif';
    ctx.fillStyle = color;
    const labelOffsetX = (scr.x > origin.x ? 10 : -20);
    const labelOffsetY = (scr.y > origin.y ? 14 : -12);
    ctx.fillText(label, scr.x + labelOffsetX, scr.y + labelOffsetY);
    ctx.restore();
  }

  drawAngleArc(real, imag, color, label) {
    const theta = Math.atan2(imag, real);
    if (Math.abs(theta) < 0.05) return;

    const ctx = this.ctx;
    const radius = Math.min(36, Math.hypot(real, imag) * this.scale * 0.4);

    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.setLineDash([2, 2]);
    ctx.beginPath();
    // In canvas coordinates, positive angle is clockwise (invert y)
    ctx.arc(this.originX, this.originY, radius, 0, -theta, theta > 0);
    ctx.stroke();

    // Angle label
    ctx.font = '10px JetBrains Mono, monospace';
    ctx.fillStyle = color;
    const midAngle = -theta / 2;
    const lx = this.originX + (radius + 12) * Math.cos(midAngle);
    const ly = this.originY + (radius + 12) * Math.sin(midAngle);
    ctx.fillText(label, lx, ly);
    ctx.restore();
  }

  drawRootsPolygon(ctx, isDark) {
    const roots = this.elements.roots;
    if (!roots || roots.length === 0) return;

    const radius = Math.hypot(roots[0].real, roots[0].imag) * this.scale;
    const color = isDark ? '#a78bfa' : '#8b5cf6';

    // Circumscribed circle
    ctx.save();
    ctx.strokeStyle = color;
    ctx.globalAlpha = 0.3;
    ctx.lineWidth = 1;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.arc(this.originX, this.originY, radius, 0, Math.PI * 2);
    ctx.stroke();

    // Regular polygon connecting roots
    ctx.globalAlpha = 0.5;
    ctx.setLineDash([]);
    ctx.beginPath();
    roots.forEach((root, idx) => {
      const scr = this.toScreen(root.real, root.imag);
      if (idx === 0) ctx.moveTo(scr.x, scr.y);
      else ctx.lineTo(scr.x, scr.y);
    });
    ctx.closePath();
    ctx.stroke();

    // Draw individual root points
    ctx.globalAlpha = 1.0;
    ctx.fillStyle = color;
    roots.forEach((root, idx) => {
      const scr = this.toScreen(root.real, root.imag);
      ctx.beginPath();
      ctx.arc(scr.x, scr.y, 4, 0, Math.PI * 2);
      ctx.fill();

      ctx.font = 'bold 11px Inter, sans-serif';
      ctx.fillText(`w${idx}`, scr.x + 8, scr.y - 8);
    });
    ctx.restore();
  }

  drawConjugateReflection(ctx) {
    const z1 = this.elements.z1;
    const conj = this.elements.conjugate;
    if (!z1 || !conj) return;

    const scr1 = this.toScreen(z1.real, z1.imag);
    const scrConj = this.toScreen(conj.real, conj.imag);

    ctx.save();
    ctx.strokeStyle = '#f59e0b';
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    ctx.moveTo(scr1.x, scr1.y);
    ctx.lineTo(scrConj.x, scrConj.y);
    ctx.stroke();

    // Conjugate vector
    this.drawVector(conj.real, conj.imag, '#f59e0b', 'z̄');
    ctx.restore();
  }

  updateElements(elements, autoScale = true) {
    this.elements = { ...this.elements, ...elements };
    this.resetView(autoScale);
  }

  clear() {
    this.elements = {
      z1: null,
      z2: null,
      result: null,
      conjugate: null,
      roots: []
    };
    this.resetView(false);
  }
}

// Global instance
window.ComplexPlane = ComplexPlane;
