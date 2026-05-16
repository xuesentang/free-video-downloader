<template>
  <div>
    <!-- 生成报告按钮 -->
    <div class="glass-card rounded-2xl border border-border p-5 sm:p-6 mb-6">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h3 class="text-base font-semibold text-text-primary">追踪报告</h3>
          <p class="text-sm text-text-muted mt-1">基于订阅博主的最新视频内容生成 AI 分析报告</p>
        </div>
        <button
          @click="handleGenerate"
          :disabled="generating || creators.length === 0"
          class="inline-flex items-center gap-2 px-5 py-2.5 btn-primary-glow text-white text-sm font-medium rounded-lg transition-all disabled:opacity-50 cursor-pointer flex-shrink-0"
        >
          <svg v-if="generating" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          {{ generating ? '生成中...' : '生成报告' }}
        </button>
      </div>
      <p v-if="genError" class="text-xs text-error mt-3">{{ genError }}</p>
    </div>

    <!-- 报告列表 -->
    <div v-if="reports.length > 0" class="space-y-4">
      <div
        v-for="report in reports"
        :key="report.id"
        class="glass-card rounded-2xl border border-border p-5 sm:p-6 hover:border-primary/30 transition-all"
      >
        <div class="flex items-start justify-between gap-4 mb-3">
          <div>
            <h4 class="text-base font-semibold text-text-primary">{{ report.title }}</h4>
            <p class="text-xs text-text-muted mt-1">
              生成时间: {{ formatDate(report.created_at) }}
              <span v-if="report.creator_count" class="ml-2">涉及 {{ report.creator_count }} 位博主</span>
            </p>
          </div>
          <button
            @click="handleDelete(report.id)"
            :disabled="deletingId === report.id"
            class="p-2 text-text-muted hover:text-error hover:bg-error/10 rounded-lg transition-colors cursor-pointer flex-shrink-0"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
        <div class="prose prose-sm max-w-none text-text-secondary">
          <div class="whitespace-pre-wrap leading-relaxed">{{ report.content }}</div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="text-center py-16">
      <svg class="w-16 h-16 mx-auto text-text-muted mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-text-muted text-sm">还没有生成过追踪报告</p>
      <p class="text-text-muted text-xs mt-1">添加博主订阅后，点击上方按钮生成 AI 分析报告</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { listReports, generateReport, deleteReport, listCreators } from '../api/tracker.js'

const reports = ref([])
const creators = ref([])
const generating = ref(false)
const deletingId = ref(null)
const genError = ref('')

onMounted(async () => {
  await loadReports()
  try {
    creators.value = await listCreators()
  } catch (err) {
    console.error('加载博主列表失败:', err)
  }
})

async function loadReports() {
  try {
    reports.value = await listReports()
  } catch (err) {
    console.error('加载报告失败:', err)
  }
}

async function handleGenerate() {
  generating.value = true
  genError.value = ''
  try {
    await generateReport()
    await loadReports()
  } catch (err) {
    genError.value = err.response?.data?.detail || '生成报告失败，请稍后重试'
  } finally {
    generating.value = false
  }
}

async function handleDelete(id) {
  deletingId.value = id
  try {
    await deleteReport(id)
    await loadReports()
  } catch (err) {
    console.error('删除失败:', err)
  } finally {
    deletingId.value = null
  }
}

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}
</script>
