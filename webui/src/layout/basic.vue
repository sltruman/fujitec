<template>
  <div>
    <van-nav-bar
      title="富士达电梯运维数据管理"
      :left-arrow="getLeft()"
      @click-left="onClickLeft"
      @click-right="onClickRight"
    >
      <template #right>
        <van-popover
          v-model="showPopover"
          trigger="click"
          :actions="actions"
          @select="onSelect"
          placement="bottom-end"
        >
          <template #reference>
            <van-icon name="wap-nav" color="#000000" size="20" />
          </template>
        </van-popover>
      </template>
    </van-nav-bar>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "basic",
  created() {
    const token = localStorage.getItem("chntek-token");
    if (!token) {
      this.$router.push({
        path: "/login"
      });
    }

    this.actions = [
      { text: "版本1.1.2", disabled: true },
      { text: "更新" },
      { text: "注销" }
    ];
  },
  data() {
    return {
      active: 0,
      activeKey: 0,
      showPopover: false,
      // 通过 actions 属性来定义菜单选项
      actions: []
    };
  },
  methods: {
    onClickLeft() {
      this.$router.go(-1);
    },
    onClickRight() { },
    getLeft() {
      const path = this.$route.name;
      switch (path) {
        case "home":
        case "gmap":
        case "history":
        case "warnings":
          return false;
        default:
          return false;
      }
    },
    async onSelect(action) {
      switch (action.text) {
        case '注销':
          window.cordova.plugins.backgroundMode.disable();
          localStorage.clear();
          this.$router.go(0);
          break;
        case "更新":
          await this.$chntek.update()
          break;
      }
    }
  }
};
</script>
<style scoped>
</style>