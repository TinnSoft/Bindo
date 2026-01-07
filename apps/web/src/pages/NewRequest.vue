<template>
  <div class="q-pa-md">
    <h2>{{ $t('new_request.title') }}</h2>
    <q-card class="q-mb-md" style="max-width: 600px">
      <q-card-section>
        <div class="q-mb-md">
          q-input
            v-model="form.company_name"
            :label="$t('new_request.company_name')"
            outlined
            dense
          />
        </div>
        <div class="q-mb-md">
          q-input
            v-model="form.nit"
            :label="$t('new_request.nit')"
            outlined
            dense
          />
        </div>
        <div class="q-mb-md">
          q-input
            v-model.number="form.contract_value"
            :label="$t('new_request.contract_value')"
            type="number"
            outlined
            dense
          />
        </div>
        <div class="q-mb-md">
          q-input
            v-model.number="form.term_months"
            :label="$t('new_request.term_months')"
            type="number"
            outlined
            dense
          />
        </div>
        <div class="q-mb-md">
          <div
            class="dropzone"
            :class="{ dragover: isDragOver }"
            @dragover.prevent="onDragOver"
            @dragenter.prevent="onDragOver"
            @dragleave.prevent="onDragLeave"
            @drop.prevent="onDrop"
            @click="openFilePicker"
          >
            <div v-if="!form.file">
              <div class="text-h6">{{ $t('new_request.drop_pdf') }}</div>
              <div class="text-subtitle2">{{ $t('new_request.drop_pdf_sub') }}</div>
            </div>
            <div v-else>
              <div class="text-subtitle1 q-mb-sm">Selected file: {{ form.file.name }}</div>
              <q-btn dense flat color="negative" :label="$t('new_request.create_upload')" @click.stop="removeFile" />
            </div>
            <input ref="fileInput" type="file" accept=".pdf" class="hidden-file-input" @change="onFileChange" style="display:none" />
          </div>
        </div>
        <q-btn
          color="primary"
          :label="$t('new_request.create_upload')"
          @click="createRequest"
          :loading="loading"
        />
      </q-card-section>
    </q-card>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'NewRequest',
  data() {
    return {
      form: {
        company_name: '',
        nit: '',
        contract_value: '',
        term_months: '',
        file: null as any,
      },
      loading: false,
      isDragOver: false,
    }
  },
  methods: {
    openFilePicker() {
      const el: any = this.$refs.fileInput
      if (el) el.click()
    },
    onFileChange(e: Event) {
      const target = e.target as HTMLInputElement
      const f = target.files && target.files[0]
      if (f && f.type === 'application/pdf') {
        this.form.file = f
      } else {
        this.$q.notify({ type: 'negative', message: 'Please select a PDF file' })
      }
    },
    onDragOver() {
      this.isDragOver = true
    },
    onDragLeave() {
      this.isDragOver = false
    },
    onDrop(e: DragEvent) {
      this.isDragOver = false
      const f = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]
      if (f && f.type === 'application/pdf') {
        this.form.file = f
      } else {
        this.$q.notify({ type: 'negative', message: 'Please drop a PDF file' })
      }
    },
    removeFile() {
      this.form.file = null
      const el: any = this.$refs.fileInput
      if (el) el.value = null
    },
    async createRequest() {
      if (!this.form.file) {
        this.$q.notify({ type: 'negative', message: 'Please select a PDF file' })
        return
      }
      this.loading = true
      try {
        // Create request
        const createResp = await axios.post('/api/v1/requests/', {
          company_name: this.form.company_name,
          nit: this.form.nit,
          contract_value: this.form.contract_value,
          term_months: this.form.term_months,
        })
        const requestId = createResp.data.id

        // Upload contract
        const formData = new FormData()
        formData.append('file', this.form.file)
        await axios.post(`/api/v1/requests/${requestId}/upload-contract`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })

        // Run extraction
        await axios.post(`/api/v1/requests/${requestId}/run-extraction`)

        this.$q.notify({ type: 'positive', message: 'Request created and processing started!' })
        this.$router.push(`/requests/${requestId}`)
      } catch (err: any) {
        console.error('Error:', err)
        this.$q.notify({ type: 'negative', message: err.response?.data?.detail || 'Error creating request' })
      } finally {
        this.loading = false
      }
    },
    onFileRejected() {
      this.$q.notify({ type: 'negative', message: 'Invalid file' })
    }
  }
})
</script>
