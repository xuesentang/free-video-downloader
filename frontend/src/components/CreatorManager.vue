<template>
  <div>
    <!-- 添加博主 -->
    <div class="glass-card rounded-2xl border border-border p-5 sm:p-6 mb-6">
      <h3 class="text-base font-semibold text-text-primary mb-3">添加博主</h3>
      <div class="flex gap-3">
        <input
          v-model="newUrl"
          type="text"
          placeholder="输入B站UP主空间链接 或 YouTube频道链接"
          class="flex-1 px-4 py-2.5 border border-border rounded-lg text-sm bg-bg-card text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary input-glow transition-all"
          :disabled="adding"
          @keyup.enter="handleAdd"
        />
        <button
          @click="handleAdd"
          :disabled="adding || !newUrl.trim()"
          class="px-5 py-2.5 btn-primary-glow text-white text-sm font-medium rounded-lg transition-all disabled:opacity-50 cursor-pointer flex-shrink-0"
        >
          {{ adding ? '添加中...' : '添加订阅' }}
        </button>
      </div>
      <p v-if="addError" class="text-xs text-error mt-2">{{ addError }}</p>
    </div>

    <!-- 博主列表 -->
    <div v-if="creators.length > 0" class="space-y-3">
      <div
        v-for="creator in creators"
        :key="creator.id"
        class="glass-card rounded-2xl border border-border p-4 sm:p-5 flex items-start gap-4 hover:border-primary/30 transition-all"
      >
        <img
          v-if="creator.avatar"
          :src="creator.avatar"
          :alt="creator.name"
          class="w-12 h-12 rounded-full object-cover flex-shrink-0 border border-border"
          @error="(e) => e.target.style.display = 'none'"
        />
        <div v-else class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 border border-primary/20">
          <span class="text-lg font-semibold text-primary">{{ creator.name[0] }}</span>
        </div>
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <h4 class="text-base font-semibold text-text-primary truncate">{{ creator.name }}</h4>
            <span class="px-2 py-0.5 text-xs rounded-full border" :class="getPlatformClass(creator.platform)">
              {{ creator.platform }}
            </span>
          </div>
          <p class="text-sm text-text-muted truncate">{{ creator.url }}</p>
          <div class="flex items-center gap-4 mt-2 text-xs text-text-muted">
            <span v-if="creator.video_count !== undefined">{{ creator.video_count }} 个视频</span>
            <span v-if="creator.last_sync">最后同步: {{ formatDate(creator.last_sync) }}</span>
          </div>
        </div>
        <button
          @click="handleRemove(creator.id)"
          :disabled="removingId === creator.id"
          class="p-2 text-text-muted hover:text-error hover:bg-error/10 rounded-lg transition-colors cursor-pointer flex-shrink-0"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-16">
      <svg class="w-16 h-16 mx-auto text-text-muted mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
      </svg>
      <p class="text-text-muted text-sm">还没有订阅任何博主</p>
      <p class="text-text-muted text-xs mt-1">在上方输入博主主页链接开始追踪</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listCreators, addCreator, removeCreator } from '../api/tracker.js'

const creators = ref([])
const newUrl = ref('')
const adding = ref(false)
const removingId = ref(null)
const addError = ref('')

onMounted(loadCreators)

async function loadCreators() {
  try {
    creators.value = await listCreators()
  } catch (err) {
    console.error('加载博主列表失败:', err)
  }
}

async function handleAdd() {
  if (!newUrl.value.trim()) return
  adding.value = true
  addError.value = ''
  try {
    await addCreator(newUrl.value.trim())
    newUrl.value = ''
    await loadCreators()
  } catch (err) {
    addError.value = err.response?.data?.detail || '添加失败，请检查链接格式'
  } finally {
    adding.value = false
  }
}

async function handleRemove(id) {
  removingId.value = id
  try {
    await removeCreator(id)
    await loadCreators()
  } catch (err) {
    console.error('删除失败:', err)
  } finally {
    removingId.value = null
  }
}

function getPlatformClass(platform) {
  const map = {
    'bilibili': 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    'youtube': 'bg-red-500/10 text-red-400 border-red-500/20',
  }
  return map[platform] || 'bg-bg-elevated text-text-muted border-border'
}

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
</script>
