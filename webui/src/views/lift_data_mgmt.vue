<template>
  <div class="main">
    <van-row type="flex" justify="center">
      <van-col span="18" class="cell">
        <a>{{ pathName }}</a>
      </van-col>
    </van-row>
    <van-row type="flex" justify="center">
      <van-col span="9" class="cell">
        <van-uploader
          :after-read="afterRead"
          :before-read="beforeRead"
          accept=".xls,.xlsx"
          :max-size="10485760"
        >
          <van-button icon="plus" type="primary">选择文件</van-button>
        </van-uploader>
      </van-col>
    </van-row>
    <van-row type="flex" justify="center">
      <van-col span="9" class="cell">
        <van-button icon="plus" type="primary">数据验证</van-button>
      </van-col>
      <van-col span="9" class="cell">
        <van-button icon="plus" type="primary">数据同步</van-button>
      </van-col>
    </van-row>
  </div>
</template>

<script>
import { getTest } from '../utils/api'
import { NavBar, Button, Icon, Uploader, Toast } from 'vant'

export default {
  name: `lift-data-mgmt`,
  components: {
    [Button.name]: Button,
    [Icon.name]: Icon,
    [Uploader.name]: Uploader,
    [Toast.name]: Toast,
    [NavBar.name]: NavBar
  },
  data() {
    return {
      pathName: ''
    }
  },
  async created() {
    const a = await getTest('cscb001')
    console.log(a)
  },
  methods: {
    beforeRead(file) {	//上传之前校验
      if (file.size > 10485760) {
        Toast('上传文件大于10m')
        return false
      }
      // if (file.type !== 'xls' && file.type !== 'xlsx') {
      //   Toast('只允许上传excel文件！')
      //   return false
      // }
      return true
    },
    afterRead(file) {
      this.pathName = file.file.name;
      // 此时可以自行将文件上传至服务器
      console.log(file);
    },
  }
}
</script>

<style scoped>
.main {
  margin-top: 2rem;
}
.cell {
  text-align: center;
}
</style>
