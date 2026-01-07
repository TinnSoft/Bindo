<template>
  <div class="q-pa-md">
    <h2>Request #{{ requestId }}</h2>
    <q-card class="q-mb-md" v-if="request.id">
      <q-card-section>
        <div class="row q-col-gutter-md">
          <div class="col-12 col-md-6">
            <div><strong>Company:</strong> {{ request.company_name }}</div>
            <div><strong>Status:</strong> <q-badge :color="statusColor(request.status)">{{ request.status }}</q-badge></div>
            <div><strong>Created:</strong> {{ formatDate(request.created_at) }}</div>
          </div>
          <div class="col-12 col-md-6">
            <div><strong>NIT:</strong> {{ request.nit }}</div>
            <div><strong>Contract Value:</strong> {{ request.contract_value }}</div>
            <div><strong>Term:</strong> {{ request.term_months }} months</div>
          </div>
        </div>
      </q-card-section>
    </q-card>

    <h3>Extracted Fields</h3>
    <q-card v-if="fields.length > 0" class="q-mb-md">
      <q-card-section>
        <div v-for="field in fields" :key="field.id" class="q-mb-md q-pa-md bg-grey-1">
          <div class="row items-center q-col-gutter-md">
            <div class="col-12 col-md-6">
              <div><strong>{{ field.key }}</strong></div>
              <div class="text-h6">{{ field.value || '(null)' }}</div>
              <div class="text-caption">Confidence: {{ (field.confidence * 100).toFixed(0) }}% | Source: {{ field.source }}</div>
            </div>
            <div class="col-12 col-md-6">
              <div class="text-caption"><strong>Evidence:</strong></div>
              <div class="text-caption">Page: {{ field.evidence_page }}</div>
              <div class="text-caption" style="word-break: break-word">{{ field.evidence_text }}</div>
            </div>
          </div>
          <div class="q-mt-md">
            <q-input
              v-model="editValues[field.id]"
              label="Override value"
              outlined
              dense
              @blur="updateField(field.id)"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>

    <div class="q-mb-md">
      <q-btn color="primary" label="Re-run Extraction" @click="rerunExtraction" :loading="loading" class="q-mr-md" />
      <q-btn color="positive" label="Mark Ready" @click="markReady" :disable="request.status === 'READY'" class="q-mr-md" />
      <q-btn color="info" label="Export JSON" @click="exportJSON" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'RequestDetail',
  data() {
    return {
      requestId: '',
      request: {} as any,
      fields: [],
      editValues: {} as any,
      loading: false,
    }
  },
  async mounted() {
    this.requestId = this.$route.params.id as string
    await this.loadRequest()
  },
  methods: {
    async loadRequest() {
      try {
        const resp = await axios.get(`/api/v1/requests/${this.requestId}`)
        this.request = resp.data
        this.fields = resp.data.extracted_fields || []
        this.fields.forEach((f: any) => {
          this.editValues[f.id] = f.value
        })
      } catch (err) {
        console.error('Error loading request:', err)
      }
    },
    async updateField(fieldId: number) {
      try {
        await axios.patch(`/api/v1/requests/${this.requestId}/fields/${fieldId}`, {
          value: this.editValues[fieldId]
        })
        this.$q.notify({ type: 'positive', message: 'Field updated' })
        await this.loadRequest()
      } catch (err) {
        console.error('Error updating field:', err)
      }
    },
    async rerunExtraction() {
      this.loading = true
      try {
        await axios.post(`/api/v1/requests/${this.requestId}/run-extraction`)
        this.$q.notify({ type: 'positive', message: 'Extraction task enqueued' })
        setTimeout(() => this.loadRequest(), 1000)
      } catch (err) {
        console.error('Error:', err)
      } finally {
        this.loading = false
      }
    },
    async markReady() {
      try {
        await axios.post(`/api/v1/requests/${this.requestId}/mark-ready`)
        this.$q.notify({ type: 'positive', message: 'Request marked as READY' })
        await this.loadRequest()
      } catch (err) {
        console.error('Error:', err)
      }
    },
    async exportJSON() {
      try {
        const resp = await axios.get(`/api/v1/requests/${this.requestId}/export`)
        const blob = new Blob([JSON.stringify(resp.data, null, 2)], { type: 'application/json' })
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `request_${this.requestId}.json`
        a.click()
      } catch (err) {
        console.error('Error:', err)
      }
    },
    statusColor(status: string) {
      const colors: any = { PENDING: 'warning', PROCESSING: 'info', REVIEW: 'blue', READY: 'positive' }
      return colors[status] || 'grey'
    },
    formatDate(date: string) {
      return new Date(date).toLocaleString()
    }
  }
})
</script>
