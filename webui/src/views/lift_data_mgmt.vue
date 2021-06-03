<template>
  <div class="main">
    <van-row type="flex" justify="center">
      <!-- <van-col span="18" class="cell">
        <a>请先选择文件，然后在数据同步</a>
      </van-col> -->
    </van-row>
    <!--     
    <van-row style="margin-top: 2rem">
      <van-grid :column-num="1">
        <van-grid-item
          v-for="value in 1"
          :key="value"
          icon="photo-o"
          :text="pathName"
        />
      </van-grid>
      <van-grid direction="horizontal" :column-num="1">
        <van-grid-item icon="plus" text="上传文件"> </van-grid-item>
      </van-grid>
    </van-row>

    <van-row type="flex" justify="center" style="margin-top: 0.5rem">
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
    </van-row> -->

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
    <van-empty description="文件上传失败" />
  </div>
</template>

<script>
import { getTest } from '../utils/api'
import { NavBar, Button, Icon, Uploader, Toast, Grid, GridItem, Image as VanImage, Empty } from 'vant'

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
  data() {
    return {
      pathName: '',
      fileList: [],
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
    submit() {
      if (!this.fileList || this.fileList.length <= 0) {
        Toast('请先选择文件，然后在数据同步')
      }
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
