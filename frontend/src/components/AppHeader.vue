<template>
  <header class="sticky top-0 z-50 glass-card border-b border-border">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <a href="/" class="flex items-center gap-3 group" title="VideoParser - 免费在线万能视频解析器">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-lg group-hover:shadow-primary/50 transition-shadow" role="img" aria-label="VideoParser Logo">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <span class="text-lg font-bold gradient-text tracking-tight">VideoParser</span>
        <span class="hidden sm:inline text-xs text-text-muted bg-bg-elevated border border-border-light px-2.5 py-0.5 rounded-full">万能视频解析</span>
      </a>
      <!-- 模式切换 -->
      <div class="flex items-center bg-bg-elevated rounded-full p-0.5 text-xs border border-border">
        <button
          @click="$emit('switch-mode', 'downloader')"
          class="px-4 py-1.5 rounded-full font-medium transition-all cursor-pointer"
          :class="mode === 'downloader' ? 'mode-active text-primary' : 'text-text-muted hover:text-text-secondary'"
        >视频解析</button>
        <button
          @click="$emit('switch-mode', 'tracker')"
          class="px-4 py-1.5 rounded-full font-medium transition-all cursor-pointer"
          :class="mode === 'tracker' ? 'mode-active text-primary' : 'text-text-muted hover:text-text-secondary'"
        >博主追踪</button>
      </div>
      <nav class="hidden md:flex items-center gap-6 text-sm text-text-secondary" aria-label="主导航" v-if="mode === 'downloader'">
        <a href="#features" class="hover:text-primary transition-colors" title="查看VideoParser功能特性">功能特性</a>
        <a href="#how-to-use" class="hover:text-primary transition-colors" title="了解如何使用VideoParser解析视频">使用教程</a>
        <a href="#comparison" class="hover:text-primary transition-colors" title="VideoParser与其他工具对比">工具对比</a>
        <a href="#pricing" class="hover:text-primary transition-colors" title="查看VideoParser套餐价格">套餐价格</a>
      </nav>
      <div class="flex items-center gap-3">
        <!-- 未登录 -->
        <template v-if="!user">
          <button @click="$emit('login')" class="hidden sm:inline-flex items-center px-4 py-2 rounded-full text-sm font-medium text-text-secondary hover:text-primary hover:bg-bg-elevated transition-colors cursor-pointer">
            登录
          </button>
          <button @click="$emit('register')" class="hidden sm:inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-medium text-white btn-primary-glow transition-all cursor-pointer">
            免费注册
          </button>
        </template>

        <!-- 已登录 -->
        <template v-else>
          <span v-if="user.is_vip" class="hidden sm:inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-yellow-400 to-orange-400 text-white shadow-sm">
            <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            VIP
          </span>

          <!-- 用户下拉菜单 -->
          <div class="relative" ref="menuRef">
            <button @click="menuOpen = !menuOpen" class="flex items-center gap-2 px-3 py-2 rounded-full hover:bg-bg-elevated transition-colors cursor-pointer">
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white text-sm font-semibold">
                {{ user.email[0].toUpperCase() }}
              </div>
              <svg class="w-4 h-4 text-text-muted transition-transform" :class="{ 'rotate-180': menuOpen }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div v-if="menuOpen" class="absolute right-0 top-full mt-2 w-56 glass-card rounded-xl border border-border shadow-xl py-2 animate-menu-in">
              <div class="px-4 py-2 border-b border-border">
                <p class="text-sm font-medium text-text-primary truncate">{{ user.email }}</p>
                <p class="text-xs text-text-muted mt-0.5">
                  {{ user.is_vip ? 'VIP 会员' : '免费用户' }}
                  <span v-if="!user.is_vip && user.remaining !== undefined" class="ml-1">· 剩余 {{ user.remaining }} 次</span>
                  <span v-if="user.is_vip && user.vip_expire_at" class="ml-1">· 到期 {{ formatDate(user.vip_expire_at) }}</span>
                </p>
              </div>
              <button v-if="!user.is_vip" @click="menuOpen = false; showVipModal = true" class="w-full text-left px-4 py-2.5 text-sm text-text-secondary hover:bg-bg-elevated transition-colors cursor-pointer flex items-center gap-2">
                <svg class="w-4 h-4 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                </svg>
                激活 VIP
              </button>
              <button @click="menuOpen = false; $emit('logout')" class="w-full text-left px-4 py-2.5 text-sm text-text-secondary hover:bg-bg-elevated transition-colors cursor-pointer flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                退出登录
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </header>

  <!-- VIP 激活弹窗 -->
  <div v-if="showVipModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm" @click.self="showVipModal = false">
    <div class="glass-card rounded-2xl max-w-sm w-full mx-4 p-6 shadow-2xl border border-border">
      <div class="flex items-center gap-3 mb-4">
        <div class="w-10 h-10 rounded-full bg-yellow-500/10 flex items-center justify-center flex-shrink-0 border border-yellow-500/20">
          <svg class="w-5 h-5 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
        </div>
        <div>
          <h4 class="font-semibold text-text-primary text-sm">激活 VIP</h4>
          <p class="text-xs text-text-muted mt-1">输入激活码升级为 VIP 会员</p>
        </div>
      </div>
      <div class="mb-4">
        <input
          v-model="vipCode"
          type="text"
          placeholder="请输入激活码"
          class="w-full px-4 py-2.5 rounded-lg border border-border bg-bg-card text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary input-glow transition-all"
          :disabled="vipLoading"
          @keyup.enter="handleActivateVip"
        />
        <p v-if="vipError" class="text-xs text-error mt-2">{{ vipError }}</p>
        <p v-if="vipSuccess" class="text-xs text-success mt-2">激活成功！您已成为 VIP 会员</p>
      </div>
      <div class="flex gap-3 justify-end">
        <button
          @click="showVipModal = false"
          class="px-4 py-2 text-sm text-text-secondary bg-bg-elevated rounded-lg hover:bg-border-light transition-colors cursor-pointer"
          :disabled="vipLoading"
        >取消</button>
        <button
          @click="handleActivateVip"
          :disabled="vipLoading || !vipCode.trim()"
          class="px-4 py-2 text-sm text-white btn-primary-glow rounded-lg disabled:opacity-50 transition-all cursor-pointer"
        >
          {{ vipLoading ? '激活中...' : '确认激活' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { activateVip } from '../api/auth.js'

defineProps({
  user: { type: Object, default: null },
  mode: { type: String, default: 'downloader' },
})

const emit = defineEmits(['login', 'register', 'logout', 'switch-mode', 'vip-activated'])

const menuOpen = ref(false)
const menuRef = ref(null)
const showVipModal = ref(false)
const vipCode = ref('')
const vipLoading = ref(false)
const vipError = ref('')
const vipSuccess = ref(false)

async function handleActivateVip() {
  vipLoading.value = true
  vipError.value = ''
  vipSuccess.value = false
  try {
    const user = await activateVip(vipCode.value.trim())
    vipSuccess.value = true
    emit('vip-activated', user)
    setTimeout(() => {
      showVipModal.value = false
      vipCode.value = ''
      vipSuccess.value = false
    }, 1500)
  } catch (err) {
    vipError.value = err.response?.data?.detail || '激活失败，请检查激活码'
  } finally {
    vipLoading.value = false
  }
}

function formatDate(isoStr) {
  if (!isoStr) return ''
  const d = new Date(isoStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function handleClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    menuOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
@keyframes menu-in {
  from { opacity: 0; transform: translateY(-4px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.animate-menu-in {
  animation: menu-in 0.15s ease-out;
}
</style>
