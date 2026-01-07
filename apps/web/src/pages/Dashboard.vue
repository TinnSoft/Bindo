<template>
  <div class="q-pa-md">
    <h2>{{ $t('nav.dashboard') }}</h2>
    <div class="row q-col-gutter-md">
      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section>
            <div class="text-h6">{{ $t('dashboard.total_requests') }}</div>
            <div class="text-h3 text-primary">{{ totalRequests }}</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section>
            <div class="text-h6">{{ $t('dashboard.pending') }}</div>
            <div class="text-h3 text-warning">{{ pendingCount }}</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section>
            <div class="text-h6">{{ $t('dashboard.in_review') }}</div>
            <div class="text-h3 text-info">{{ reviewCount }}</div>
          </q-card-section>
        </q-card>
      </div>
      <div class="col-12 col-md-3">
        <q-card>
          <q-card-section>
            <div class="text-h6">{{ $t('dashboard.ready') }}</div>
            <div class="text-h3 text-positive">{{ readyCount }}</div>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <div class="q-mt-md">
      <div v-if="loading" class="row q-col-gutter-md">
        <div class="col-12 col-md-4" v-for="n in 3" :key="n">
          <q-skeleton type="card" animated />
        </div>
      </div>
      <div v-else-if="totalRequests === 0" class="empty-state q-mt-md">
        <div class="text-h6 q-mb-sm">{{ $t('dashboard.no_activity') }}</div>
        <div class="text-subtitle2 q-mb-md">{{ $t('dashboard.create_request') }}</div>
        <q-btn color="primary" :label="$t('dashboard.create_request')" @click="$router.push('/requests/new')" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'Dashboard',
  data() {
    return {
      totalRequests: 0,
      pendingCount: 0,
      reviewCount: 0,
      readyCount: 0,
      loading: false,
    }
  },
  async mounted() {
    this.loading = true
    try {
      const resp = await axios.get('/api/v1/requests/')
      const reqs = resp.data
      this.totalRequests = reqs.length
      this.pendingCount = reqs.filter((r: any) => r.status === 'PENDING').length
      this.reviewCount = reqs.filter((r: any) => r.status === 'REVIEW').length
      this.readyCount = reqs.filter((r: any) => r.status === 'READY').length
    } catch (err) {
      console.error('Error loading KPIs:', err)
    } finally {
      this.loading = false
    }
  }
})
</script>
