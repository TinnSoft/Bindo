<template>
  <div class="q-pa-md">
    <h2>{{ $t('requests.title') }}</h2>

    <div v-if="loading">
      <q-skeleton type="heading" animated class="q-mb-md" />
      <div class="row q-col-gutter-md">
        <div class="col-12 col-md-6" v-for="n in 2" :key="n">
          <q-card>
            <q-card-section>
              <q-skeleton type="text" animated />
              <q-skeleton type="text" animated />
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <div v-else>
      <div v-if="requests.length === 0" class="empty-state">
        <q-avatar size="80px" class="q-mb-md"><q-icon name="description" size="48px"/></q-avatar>
        <div class="text-h6 q-mb-sm">{{ $t('requests.no_requests') }}</div>
        <div class="text-subtitle2 q-mb-md">{{ $t('requests.create_request') }}</div>
        <q-btn color="primary" :label="$t('requests.create_request')" @click="$router.push('/requests/new')" />
      </div>

      <q-table
        :rows="requests"
        :columns="columns"
        row-key="id"
        :row-class="rowClass"
        @row-click="goToDetail"
      >
        <template v-slot:body-cell-status="props">
          <q-td :props="props">
            <q-chip :class="['status-chip']" :color="statusColor(props.row.status)" text-color="white">
              {{ props.row.status }}
            </q-chip>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn flat dense small color="primary" :label="$t('requests.view')" @click.stop="goToDetail(props.row)" />
          </q-td>
        </template>
      </q-table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'

export default defineComponent({
  name: 'Requests',
  data() {
    return {
      requests: [],
      loading: false,
      columns: [
        { name: 'id', label: 'ID', field: 'id', align: 'left' },
        { name: 'company_name', label: 'Company', field: 'company_name' },
        { name: 'status', label: 'Status', field: 'status' },
        { name: 'created_at', label: 'Created', field: 'created_at' },
        { name: 'actions', label: 'Actions' },
      ]
    }
  },
  async mounted() {
    await this.loadRequests()
  },
  methods: {
    async loadRequests() {
      this.loading = true
      try {
        const resp = await axios.get('/api/v1/requests/')
        this.requests = resp.data
      } catch (err) {
        console.error('Error loading requests:', err)
      } finally {
        this.loading = false
      }
    },
    goToDetail(row: any) {
      this.$router.push(`/requests/${row.id}`)
    },
    statusColor(status: string) {
      switch ((status || '').toUpperCase()) {
        case 'PENDING': return 'amber'
        case 'REVIEW': return 'blue'
        case 'READY': return 'green'
        default: return 'grey'
      }
    },
    rowClass(row: any) {
      return ''
    }
  }
})
</script>
