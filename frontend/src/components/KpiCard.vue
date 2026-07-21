<template>
  <div class="kpi-card card" :class="[variant, { 'animate-fade-in-up': animate }]">
    <div v-if="icon || $slots.icon" class="kpi-card__icon" :style="gradient ? `background: ${gradient}` : ''">
      <slot name="icon">
        <span v-if="icon" v-html="icon"></span>
      </slot>
    </div>
    <div class="kpi-card__body">
      <span class="kpi-card__value">{{ value }}</span>
      <span class="kpi-card__label">{{ label }}</span>
    </div>
    <span v-if="change" class="kpi-card__change" :class="up ? 'up' : 'down'">
      {{ up ? '↑' : '↓' }} {{ change }}
    </span>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [String, Number], required: true },
  icon: { type: String, default: '' },
  gradient: { type: String, default: '' },
  change: { type: String, default: '' },
  up: { type: Boolean, default: true },
  variant: { 
    type: String, 
    default: 'detailed',
    validator: (v) => ['detailed', 'simple'].includes(v)
  },
  animate: { type: Boolean, default: true }
})
</script>

<style scoped>
.kpi-card {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-4) var(--sp-6);
  transition: transform 0.2s, box-shadow 0.2s;
}

@media (max-width: 768px) {
  .kpi-card {
    padding: var(--sp-3) var(--sp-4);
  }
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--clr-primary);
}

.kpi-card__icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: var(--clr-surface-3);
}

.kpi-card__icon :deep(svg) {
  width: 20px;
  height: 20px;
  stroke: white;
}

.kpi-card__body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.kpi-card__value {
  font-family: var(--font-heading);
  font-size: clamp(1.2rem, 4vw, 1.6rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  color: var(--clr-text);
  line-height: 1.2;
}

.kpi-card__label {
  font-size: 0.8rem;
  color: var(--clr-text-muted);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.kpi-card__change {
  font-size: 0.8rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.kpi-card__change.up {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.kpi-card__change.down {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

/* Simple Variant */
.simple {
  padding: 1.25rem;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.simple .kpi-card__value {
  font-size: clamp(1.1rem, 3.5vw, 1.5rem);
}

.simple .kpi-card__label {
  font-size: 0.7rem;
  margin-top: 2px;
}
</style>
