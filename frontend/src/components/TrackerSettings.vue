<template>
  <div class="glass-card rounded-2xl border border-border p-6 max-w-lg">
    <h3 class="text-base font-semibold text-text-primary mb-5">定时追踪设置</h3>

    <div v-if="loading" class="text-center py-8 text-text-muted">加载中...</div>

    <template v-else>
      <!-- 开关 -->
      <div class="flex items-center justify-between mb-5">
        <div>
          <div class="text-sm font-medium text-text-primary">启用定时追踪</div>
          <div class="text-xs text-text-muted mt-0.5">系统将按设定时间自动生成追踪报告</div>
        </div>
        <button
          @click="toggleEnabled"
          class="relative w-11 h-6 rounded-full transition-colors cursor-pointer"
          :class="settings.enabled === 'true' ? 'bg-primary' : 'bg-border-light'"
        >
          <span
            class="absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform"
            :class="settings.enabled === 'true' ? 'translate-x-[22px]' : 'translate-x-0.5'"
          />
        </button>
      </div>

      <!-- 定时时间 -->
      <div class="mb-5">
        <label class="text-sm font-medium text-text-primary block mb-1.5">定时生成时间</label>
        <input
          v-model="settings.schedule_time"
          type="time"
          class="px-3 py-2 border border-border rounded-lg text-sm bg-bg-card text-text-primary focus:outline-none focus:ring-2 focus:ring-primary/30 input-glow transition-all"
        />
        <p class="text-xs text-text-muted mt-1">每天在此时间自动生成追踪报告</p>
      </div>

      <!-- 追踪时间范围 -->
      <div class="mb-6">
        <label class="text-sm font-medium text-text-primary block mb-1.5">追踪时间范围</label>
        <select
          v-model="settings.time_range_hours"
          class="px-3 py-2 border border-border rounded-lg text-sm bg-bg-card text-text-primary focus:outline-none focus:ring-2 focus:ring-primary/30 input-glow transition-all"
        >
          <option value="12">最近 12 小时</option>
          <option value="24">最近 24 小时</option>
          <option value="48">最近 48 小时</option>
          <option value="72">最近 72 小时</option>
        </select>
        <p class="text-xs text-text-muted mt-1">报告将包含此时间范围内的新视频</p>
      </div>

      <!-- 保存按钮 -->
      <button
        @click="handleSave"
        :disabled="saving"
        class="px-5 py-2.5 btn-primary-glow text-white text-sm font-medium rounded-lg transition-all disabled:opacity-50 cursor-pointer"
      >
        {{ saving ? '保存中...' : '保存设置' }}
      </button>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSettings, updateSettings } from '../api/tracker.js'

defineProps({
  user: { type: Object, default: null },
})

const emit = defineEmits(['need-login'])

const loading = ref(false)
const saving = ref(false)
const settings = reactive({
  schedule_time: '09:00',
  time_range_hours: '24',
  enabled: 'true',
})

onMounted(() => { loadSettings() })

async function loadSettings() {
  loading.value = true
  try {
    const res = await getSettings()
    if (res.success && res.data) {
      settings.schedule_time = res.data.schedule_time || '09:00'
      settings.time_range_hours = res.data.time_range_hours || '24'
      settings.enabled = res.data.enabled || 'true'
    }
  } catch (err) {
    if (err.response?.status === 401) emit('need-login')
  } finally {
    loading.value = false
  }
}

function toggleEnabled() {
  settings.enabled = settings.enabled === 'true' ? 'false' : 'true'
}

async function handleSave() {
  saving.value = true
  try {
    const res = await updateSettings({
      scheduleTime: settings.schedule_time,
      timeRangeHours: parseInt(settings.time_range_hours),
      enabled: settings.enabled,
    })
    if (res.success) alert('设置已保存')
  } catch (err) {
    alert('保存失败: ' + (err.response?.data?.detail || err.message))
  } finally {
    saving.value = false
  }
}
</script>
