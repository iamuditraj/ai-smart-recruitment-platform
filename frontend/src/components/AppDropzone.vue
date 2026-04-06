<template>
  <div 
    class="upload-zone card" 
    :class="[{ 'dragging': isDragging }, customClass]"
    @dragover.prevent="isDragging = true"
    @dragleave.prevent="isDragging = false"
    @drop.prevent="onDrop"
  >
    <slot></slot>
    <input
      :id="inputId"
      type="file"
      :multiple="multiple"
      :accept="accept"
      style="display: none;"
      @change="onFileChange"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  inputId: { type: String, default: 'file-input' },
  multiple: { type: Boolean, default: false },
  accept: { type: String, default: '*/*' },
  customClass: { type: String, default: '' }
})

const emit = defineEmits(['files-selected'])

const isDragging = ref(false)

function onFileChange(e) {
  emit('files-selected', Array.from(e.target.files))
  // Reset input so the same file can be selected again if needed
  e.target.value = null
}

function onDrop(e) {
  isDragging.value = false
  emit('files-selected', Array.from(e.dataTransfer.files))
}
</script>

<style scoped>
.upload-zone {
  position: relative;
  border: 2px dashed var(--clr-border);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1.5rem;
  background: var(--clr-surface);
  transition: all 0.3s;
}
.upload-zone.dragging {
  border-color: var(--clr-primary);
  background: var(--clr-surface-2);
}
</style>
