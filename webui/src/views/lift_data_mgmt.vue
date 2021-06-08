<template>
  <div class="main">
    <van-row type="flex" justify="center"> </van-row>

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
    <van-collapse v-if="statusData.status" v-model="activeNames">
      <van-collapse-item name="1" title="同步状态" :value="getStatus()">
        <van-list
          v-model="loading"
          :finished="finished"
          finished-text="没有更多了"
          loading-text="加载上传失败数据中..."
          @load="onLoad"
        >
          <van-cell title="成功数量" :value="statusData.count" />
          <!-- <van-cell title="失败数量" :value="statusData.errors.length" /> -->
          <van-divider
            :style="{
              color: '#1989fa',
              borderColor: '#1989fa',
              padding: '0 16px',
            }"
            >无法定位的地址</van-divider
          >
          <van-cell v-for="item in list" :key="item" :title="item" />
        </van-list>
      </van-collapse-item>
    </van-collapse>
  </div>
</template>

<script>
import { uploadurl, syncDataStatus } from '../utils/api'
import {
  NavBar, Button, Icon, Uploader, Toast, Grid, GridItem, Image as VanImage, Empty, Collapse, CollapseItem, Cell,
  Row, Divider,
  Col, List
} from 'vant'
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
    [Collapse.name]: Collapse,
    [CollapseItem.name]: CollapseItem,
    [Row.name]: Row,
    [Col.name]: Col,
    [List.name]: List,
    [Divider.name]: Divider,
    [Cell.name]: Cell,
    [VanImage.name]: VanImage
  },
  data() {
    return {
      pathName: '',
      fileList: [],
      fileData: null,
      msg: '',
      statusData: {
        count: 0,
        date: null,
        status: '',
        errors: []
      },
      activeNames: [],
      list: [],
      loading: false,
      finished: false,
    }
  },
  created() {
    this.loadStatus()
  },
  methods: {
    loadStatus() {
      this.list = [];
      this.statusData = {
        count: 0,
        date: null,
        status: '',
        errors: []
      }
      syncDataStatus().then(res => {
        if (res) {
          this.statusData = res.val
        }
      })
    },
    beforeRead(file) {
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
    afterRead(file) {
      this.pathName = file.file.name
      this.fileData = file
    },
    submit() {
      if (!this.fileList || this.fileList.length <= 0) {
        Toast('请先选择文件，然后在数据同步')
        return
      }
      this.upd()
    },
    upd() {
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
          this.loadStatus()
        } else {
          Toast('文件上传失败：' + res.data.err)
        }
        this.fileList = []
      })
    },
    getStatus() {
      if (this.statusData) {
        switch (this.statusData.status) {
          case 'synced':
            return '同步结束'
            break;
          case 'syncing':
            return '同步中'
            break;
          default:
            return '1'

        }
      }
    },
    onLoad() {
      // 异步更新数据
      // setTimeout 仅做示例，真实场景中一般为 ajax 请求
      setTimeout(() => {
        for (let i = 0; i < 10; i++) {
          if (this.list.length < this.statusData.errors.length) {
            this.list.push(this.statusData.errors[this.list.length]);
            break;
          }
        }

        // 加载状态结束
        this.loading = false;

        // 数据全部加载完成
        if (this.list.length >= this.statusData.errors.length) {
          this.finished = true;
        }
      }, 1000);
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
