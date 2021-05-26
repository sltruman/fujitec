<template>
  <div>
    <van-nav-bar
      title="富士达电梯运维数据管理"
    />
  </div>
</template>

<script>
import {getTest} from '../utils/api'
import {NavBar} from 'vant'

export default {
  name: `lift-data-mgmt`,
  components: {
    [NavBar.name]: NavBar
  },
  async created () {
    const a = await getTest('cscb001')
    console.log(a)
  }
}
</script>

<style scoped>

</style>
