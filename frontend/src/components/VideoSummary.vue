<template>
  <div class="glass-card rounded-2xl border border-border shadow-lg overflow-hidden h-full flex flex-col">
    <!-- 标签页 -->
    <div class="flex border-b border-border bg-bg-elevated">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        :class="[
          'flex-1 py-3 px-4 text-sm font-medium transition-all cursor-pointer border-b-2',
          activeTab === tab.key
            ? 'border-primary text-primary'
            : 'border-transparent text-text-muted hover:text-text-secondary hover:bg-bg-card'
        ]"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 内容区 -->
    <div class="flex-1 overflow-y-auto p-5 sm:p-6">
      <!-- 摘要 -->
      <div v-if="activeTab === 'summary'">
        <div v-if="!summaryData.summary" class="flex flex-col items-center justify-center py-12 text-center">
          <svg class="w-10 h-10 text-text-muted mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          <p class="text-text-muted text-sm mb-4">暂无 AI 总结内容</p>
          <button
            @click="$emit('summarize')"
            :disabled="summarizing"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full btn-primary-glow text-white text-sm font-medium transition-all disabled:opacity-50 cursor-pointer"
          >
            <svg v-if="summarizing" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ summarizing ? '总结中...' : '生成 AI 总结' }}
          </button>
        </div>
        <div v-else>
          <div class="prose prose-sm max-w-none text-text-primary">
            <div class="whitespace-pre-wrap leading-relaxed">{{ summaryData.summary }}</div>
          </div>
          <div v-if="summaryData.keywords?.length" class="mt-5 pt-4 border-t border-border">
            <h4 class="text-sm font-medium text-text-primary mb-2">关键词</h4>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="kw in summaryData.keywords"
                :key="kw"
                class="px-3 py-1 rounded-full text-xs bg-primary/10 text-primary border border-primary/20"
              >{{ kw }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 字幕 -->
      <div v-if="activeTab === 'subtitles'">
        <div v-if="!summaryData.subtitles" class="flex flex-col items-center justify-center py-12 text-center">
          <svg class="w-10 h-10 text-text-muted mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
          </svg>
          <p class="text-text-muted text-sm">暂无字幕内容</p>
        </div>
        <div v-else class="prose prose-sm max-w-none text-text-primary">
          <div class="whitespace-pre-wrap leading-relaxed">{{ summaryData.subtitles }}</div>
        </div>
      </div>

      <!-- 思维导图 -->
      <div v-if="activeTab === 'mindmap'">
        <div v-if="!summaryData.mindmap" class="flex flex-col items-center justify-center py-12 text-center">
          <svg class="w-10 h-10 text-text-muted mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0121 18.382V7.618a1 1 0 01-.553-.894L15 7m0 13V7m0 0L9 7" />
          </svg>
          <p class="text-text-muted text-sm mb-4">暂无思维导图</p>
          <button
            @click="$emit('summarize')"
            :disabled="summarizing"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full btn-primary-glow text-white text-sm font-medium transition-all disabled:opacity-50 cursor-pointer"
          >
            <svg v-if="summarizing" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ summarizing ? '生成中...' : '生成思维导图' }}
          </button>
        </div>
        <div v-else>
          <pre class="text-xs text-text-secondary bg-bg-elevated p-4 rounded-xl overflow-x-auto border border-border">{{ summaryData.mindmap }}</pre>
        </div>
      </div>

      <!-- AI 问答 -->
      <div v-if="activeTab === 'chat'" class="flex flex-col h-full">
        <div ref="chatContainer" class="flex-1 overflow-y-auto space-y-3 mb-4 max-h-[400px]">
          <div v-for="(msg, i) in chatMessages" :key="i" class="flex gap-3" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
            <div
              class="max-w-[80%] rounded-xl px-4 py-2.5 text-sm"
              :class="msg.role === 'user' ? 'bg-primary text-white rounded-br-sm' : 'bg-bg-elevated text-text-primary rounded-bl-sm border border-border'"
            >
              {{ msg.content }}
            </div>
          </div>
          <div v-if="chatLoading" class="flex gap-3 justify-start">
            <div class="bg-bg-elevated rounded-xl rounded-bl-sm px-4 py-2.5 text-sm text-text-muted border border-border">
              <span class="inline-flex items-center gap-1">
                <span class="w-1.5 h-1.5 bg-primary rounded-full animate-bounce"></span>
                <span class="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style="animation-delay: 0.1s"></span>
                <span class="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
              </span>
            </div>
          </div>
        </div>
        <div class="flex gap-2">
          <input
            v-model="chatInput"
            type="text"
            placeholder="针对视频内容提问..."
            class="flex-1 px-4 py-2.5 rounded-xl border border-border bg-bg-card text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary input-glow transition-all"
            @keyup.enter="sendChat"
          />
          <button
            @click="sendChat"
            :disabled="!chatInput.trim() || chatLoading"
            class="px-4 py-2.5 rounded-xl btn-primary-glow text-white text-sm font-medium transition-all disabled:opacity-50 cursor-pointer"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { chatWithVideo } from '../api/summarize.js'

const props = defineProps({
  summaryData: { type: Object, default: () => ({}) },
  summarizing: Boolean,
})
const emit = defineEmits(['summarize'])

const tabs = [
  { key: 'summary', label: '摘要' },
  { key: 'subtitles', label: '字幕' },
  { key: 'mindmap', label: '思维导图' },
  { key: 'chat', label: 'AI 问答' },
]

const activeTab = ref('summary')
const chatMessages = ref([])
const chatInput = ref('')
const chatLoading = ref(false)
const chatContainer = ref(null)

async function sendChat() {
  const question = chatInput.value.trim()
  if (!question || chatLoading.value) return

  chatMessages.value.push({ role: 'user', content: question })
  chatInput.value = ''
  chatLoading.value = true

  await nextTick()
  scrollToBottom()

  try {
    let answer = ''
    await chatWithVideo('', question, props.summaryData.subtitles || '', {
      message: (data) => { answer += data },
      done: () => {},
    })
    chatMessages.value.push({ role: 'assistant', content: answer || '抱歉，没有获取到回答。' })
  } catch (err) {
    chatMessages.value.push({ role: 'assistant', content: '抱歉，发生了错误，请稍后重试。' })
  } finally {
    chatLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

function scrollToBottom() {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

watch(() => props.summaryData, () => {
  chatMessages.value = []
  chatInput.value = ''
})
</script>
