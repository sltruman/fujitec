<template>

</template>

<script>
import {getTest} from '../utils/api'

export default {
  name: `lift-data-mgmt`,
  async created () {
    const a = await getTest('cscb001')
    console.log(a)
  }
}
</script>

<style scoped>

</style>
