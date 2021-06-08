<template>
  <div class="main">
    <van-row type="flex" justify="center">
    </van-row>

    <van-row type="flex" justify="center" style="margin-top: 1rem">
      <van-uploader
        v-model="fileList"
        :after-read="afterRead"
        :before-read="beforeRead"
        :max-size="10485760"
        upload-icon="plus"
        max-count="1"
        upload-text="点击选择文件"
        accept=".xls,.xlsx"
      />
    </van-row>
    <van-row type="flex" justify="center" style="margin-top: 1rem">
      <van-col span="9" class="cell">
        <van-button type="primary" @click="submit">数据同步</van-button>
      </van-col>
    </van-row>
    {{ msg }}
    <!--    <van-empty description="文件上传失败"/>-->
  </div>
</template>

<script>
import {uploadurl} from '../utils/api'
import {NavBar, Button, Icon, Uploader, Toast, Grid, GridItem, Image as VanImage, Empty} from 'vant'
import axios from 'axios'

export default {
  name: `lift-data-mgmt`,
  components: {
    [Button.name]: Button,
    [Icon.name]: Icon,
    [Uploader.name]: Uploader,
    [Toast.name]: Toast,
    [GridItem.name]: GridItem,
    [Grid.name]: Grid,
    [NavBar.name]: NavBar,
    [Empty.name]: Empty,
    [VanImage.name]: VanImage
  },
  data () {
    return {
      pathName: '',
      fileList: [],
      fileData: null,
      msg: ''
    }
  },
  async created () {
  },
  methods: {
    beforeRead (file) {
      // 上传之前校验
      if (file.size > 10485760) {
        Toast('上传文件大于10m')
        return false
      }
      const fileType = file.name.substring(file.name.lastIndexOf('.') + 1)
      if (fileType !== 'xls' && fileType !== 'xlsx') {
        Toast('只允许上传excel文件！')
        return false
      }
      return true
    },
    afterRead (file) {
      this.pathName = file.file.name
      this.fileData = file
    },
    submit () {
      if (!this.fileList || this.fileList.length <= 0) {
        Toast('请先选择文件，然后在数据同步')
        return
      }
      this.upd()
    },
    upd () {
      let formData = new FormData()
      formData.append('file', new Blob([this.fileList]))
      axios({
        method: 'post',
        url: uploadurl,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data' // 关键
        }
      }).then((res) => {
        if (res.data.val) {
          Toast('文件上传成功')
        } else {
          Toast('文件上传失败：' + res.data.err)
        }
        this.fileList = []
      })
    }
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
