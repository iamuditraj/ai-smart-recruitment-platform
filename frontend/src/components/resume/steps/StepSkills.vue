<template>
  <div class="form-step">
    <h2 class="step-title">Skills</h2>
    <p class="step-desc">Type a skill and press <kbd>Enter</kbd> or comma to add it.</p>

    <!-- Technical Skills -->
    <div class="form-group">
      <label class="form-label" for="rg-tech-skill-input">Technical Skills</label>
      <div class="rg-tag-input">
        <div class="rg-tag-input__tags">
          <span
            v-for="skill in store.formData.skills.technical"
            :key="skill"
            class="rg-skill-tag"
            :id="`rg-tech-tag-${skill}`"
          >
            {{ skill }}
            <button @click="store.removeSkill('technical', skill)" class="rg-tag-remove" :aria-label="`Remove ${skill}`">×</button>
          </span>
        </div>
        <input
          id="rg-tech-skill-input"
          type="text"
          class="rg-tag-field"
          v-model="techInput"
          placeholder="e.g. Python, TensorFlow..."
          @keydown="handleTechKeydown"
        />
      </div>
      <p class="rg-input-hint">{{ store.formData.skills.technical.length }} skills added</p>
    </div>

    <!-- Soft Skills -->
    <div class="form-group" style="margin-top: var(--sp-6)">
      <label class="form-label" for="rg-soft-skill-input">Soft Skills</label>
      <div class="rg-tag-input">
        <div class="rg-tag-input__tags">
          <span
            v-for="skill in store.formData.skills.soft"
            :key="skill"
            class="rg-skill-tag rg-skill-tag--soft"
            :id="`rg-soft-tag-${skill}`"
          >
            {{ skill }}
            <button @click="store.removeSkill('soft', skill)" class="rg-tag-remove">×</button>
          </span>
        </div>
        <input
          id="rg-soft-skill-input"
          type="text"
          class="rg-tag-field"
          v-model="softInput"
          placeholder="e.g. Leadership, Communication..."
          @keydown="handleSoftKeydown"
        />
      </div>
      <p class="rg-input-hint">{{ store.formData.skills.soft.length }} skills added</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useResumeStore } from '../../../stores/resume.js'

const store = useResumeStore()

const techInput = ref('')
const softInput = ref('')

function addTechSkill() {
  if (techInput.value.trim() !== '') {
    store.addSkill('technical', techInput.value)
    techInput.value = ''
  }
}

function addSoftSkill() {
  if (softInput.value.trim() !== '') {
    store.addSkill('soft', softInput.value)
    softInput.value = ''
  }
}

function handleTechKeydown(e) {
  if (e.key === ',' || e.key === 'Enter') {
    e.preventDefault()
    addTechSkill()
  }
}

function handleSoftKeydown(e) {
  if (e.key === ',' || e.key === 'Enter') {
    e.preventDefault()
    addSoftSkill()
  }
}
</script>

<style scoped>
/* Tag Input */
.rg-tag-input {
  background: var(--clr-surface-2);
  border: 1px solid var(--clr-border);
  border-radius: var(--radius-md);
  padding: var(--sp-3);
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.rg-tag-input:focus-within {
  border-color: var(--clr-primary);
  box-shadow: 0 0 0 3px rgba(99,102,241,0.15);
}

.rg-tag-input__tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-2);
}

.rg-skill-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.3);
  border-radius: var(--radius-full);
  padding: 0.2rem 0.6rem 0.2rem 0.8rem;
  font-size: 0.8rem;
  font-weight: 600;
  color: #a5b4fc;
}

.rg-skill-tag--soft {
  background: rgba(16,185,129,0.1);
  border-color: rgba(16,185,129,0.3);
  color: #6ee7b7;
}

.rg-tag-remove {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  opacity: 0.7;
  padding: 0;
  transition: opacity var(--transition-fast);
}

.rg-tag-remove:hover { opacity: 1; }

.rg-tag-field {
  background: none;
  border: none;
  outline: none;
  color: var(--clr-text);
  font-size: 0.875rem;
  font-family: var(--font-body);
  width: 100%;
  padding: var(--sp-1) var(--sp-2);
}

.rg-tag-field::placeholder { color: var(--clr-text-muted); }

.rg-input-hint {
  font-size: 0.75rem;
  color: var(--clr-text-muted);
  margin-top: var(--sp-1);
}

kbd {
  background: var(--clr-surface-3);
  border: 1px solid var(--clr-border-hover);
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  font-size: 0.8em;
  font-family: monospace;
}
</style>
