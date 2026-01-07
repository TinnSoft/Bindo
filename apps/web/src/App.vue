<template>
  <q-layout view="hHh lpR ffd">
    <!-- Header -->
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-toolbar-title>{{ $t('app.title') }}</q-toolbar-title>
        <div class="text-subtitle2">{{ $t('app.subtitle') }}</div>
      </q-toolbar>
    </q-header>

    <!-- Sidebar Navigation -->
    <q-drawer side="left" show-if-above bordered class="bg-white">
      <q-list>
        <q-item clickable :to="'/'" class="q-mb-md" active-class="bg-blue-1">
          <q-item-section avatar>
            <q-icon name="dashboard" size="lg" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('nav.dashboard') }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable :to="'/requests'" class="q-mb-md" active-class="bg-blue-1">
          <q-item-section avatar>
            <q-icon name="list" size="lg" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('nav.requests') }}</q-item-label>
          </q-item-section>
        </q-item>
        <q-item clickable :to="'/requests/new'" class="q-mb-md" active-class="bg-blue-1">
          <q-item-section avatar>
            <q-icon name="add" size="lg" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ $t('nav.new_request') }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <!-- Page Content -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({ name: 'App' })
</script>

<style>
/* Global UI consistency overrides */
html, body, #q-app {
  font-family: Roboto, "Helvetica Neue", Arial, sans-serif;
}
h2 {
  font-weight: 300;
  font-size: 2.5rem;
  margin: 0 0 1.25rem 0;
}
.q-pa-md {
  padding: 1rem !important;
}
/* Table row hover */
.q-table__grid tbody tr:hover {
  background-color: rgba(0,0,0,0.02);
}
/* Primary button consistent look */
.q-btn--primary {
  border-radius: 6px;
  padding: 8px 16px;
  font-weight: 500;
}
/* Status chip */
.status-chip {
  min-width: 80px;
  text-align: center;
  font-weight: 600;
}

/* Dropzone */
.dropzone {
  border: 2px dashed rgba(0,0,0,0.12);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
}
.dropzone.dragover {
  background-color: rgba(0,0,0,0.03);
  border-color: rgba(0, 122, 255, 0.6);
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 40px 20px;
}

</style>
