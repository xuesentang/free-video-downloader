<template>
  <div class="flex-1 bg-bg-main">
    <!-- 顶部 Tab 导航 -->
    <div class="border-b border-border bg-bg-elevated">
      <div class="max-w-5xl mx-auto px-4 sm:px-6">
        <div class="flex gap-6">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            class="py-3 px-1 text-sm font-medium transition-all cursor-pointer border-b-2"
            :class="activeTab === tab.key
              ? 'border-primary text-primary'
              : 'border-transparent text-text-muted hover:text-text-secondary'"
          >
            {{ tab.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- 内容区 -->
    <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
      <CreatorManager v-if="activeTab === 'creators'" />
      <ReportList v-else-if="activeTab === 'reports'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CreatorManager from './CreatorManager.vue'
import ReportList from './ReportList.vue'

const tabs = [
  { key: 'creators', label: '我的订阅' },
  { key: 'reports', label: '追踪报告' },
]
const activeTab = ref('creators')
</script>
