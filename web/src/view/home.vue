<template>
	<div style="height: 100%;">
		<!-- 同步动画 -->
		<van-loading color="#0094ff" size="40px" text-size="16px" vertical v-if="syncLoading" class="loading-box">正在同步数据,请耐心等待...</van-loading>
		<div class="toolbar" v-if="positionLoading">正在定位...</div>
		<!-- 导航栏 -->
		<van-nav-bar title="富士达" :left-arrow="editVisible" @click-left="onClickLeft" v-if="!syncLoading" />
		<!-- 地图 -->
		<div class="map-box" v-show="!editVisible">
			<el-amap vid="amapDemo" viewMode="3D" :plugin="plugin" :zoom="zoom" :resizeEnable="true" :isHotspot="true" :center="center">
				<el-amap-marker
					v-for="(item, index) in markerGroups"
					:key="index"
					:position="[item[0], item[1]]"
					:visible="true"
					:content="getContentHtml(item)"
					:draggable="false"
					:events="events"
					:extData="item"
				></el-amap-marker>
			</el-amap>
			<!-- 编辑框 -->
			<van-popup v-model="showPicker" :close-on-popstate="true" :overlay="false" position="bottom">
				<van-picker
					show-toolbar
					v-if="showPicker"
					:title="currentLocation"
					value-key="elevatorsName"
					:columns="elevatorsColums"
					@confirm="elevatorsClick"
					@cancel="cancelChange"
				></van-picker>
			</van-popup>
		</div>
		<!-- 表单 -->
		<editForm v-if="editVisible" :formData="formData" @change="editFormChange"></editForm>
	</div>
</template>

<script>
import editForm from '@/components/editForm';
export default {
	name: 'home',
	components: {
		editForm
	},
	data() {
		let self = this;
		return {
			syncLoading: true,
			positionLoading: false,
			// 缩放级别
			zoom: 17,
			center: [120.011574, 30.286369],
			//工具插件
			plugin: [
				//一些工具插件
				{
					pName: 'Geolocation', //定位
					events: {
						init(o) {
							// o 是高德地图定位插件实例
							o.getCurrentPosition((status, result) => {
								if (result && result.position) {
									self.center = [result.position.lng, result.position.lat]; //设置坐标
								}
                self.positionLoading = false;
							});
						}
					}
				},
				{
					pName: 'ToolBar' //缩放
				}
			],
			// 定义点坐标组数组
			markerGroups: [],
			events: {
				click: e => {
					this.$nextTick(() => {
						this.popupClick(e.target.w.extData);
					});
				}
			},
			//编辑框
			showPicker: false,
			elevatorsColums: [],
			currentLocation: '',
			formData: {},
			editVisible: false
		};
	},
	created() {
		this.getSyncedStatus();
	},
	methods: {
		//返回按钮事件
		onClickLeft() {
			this.editVisible = false;
			this.showPicker = true;
			this.getSyncedStatus();
		},
		//获取同步数据状态
		getSyncedStatus() {
			this.$http
				.getSyncedStatus()
				.then(res => {
					
					let lastDate = localStorage.getItem('lastDate');
					if (res.data.val != lastDate) {
						localStorage.removeItem('elevators');
						localStorage.setItem('lastDate', res.data.val);
						this.getElevatorsStatus();
					} else {
						this.positionLoading = true;
						this.getLocalStorage();
					}
				})
				.catch(() => {
					this.syncLoading = false;
				});
		},
		//获取本地数据
		getLocalStorage() {
			this.markerGroups = JSON.parse(localStorage.getItem('elevators'));
			this.syncLoading = false;
		},
		//获取地图标识点
		getElevatorsStatus() {
			this.$http.getElevatorsStatus().then(res => {
				this.positionLoading = true;
				localStorage.setItem('elevators', JSON.stringify(res.data.val));
				this.getLocalStorage();
			})
		},
		//显示数字图标
		getContentHtml(val) {
			let number = val[2];
			let status = val[3];
			if (number) {
				// 未避免被简书转化未设置img的src属性
				let colorOptions = {
					代理商保养: 'blue_bg',
					第三方保养: 'blue_bg',
					我方保养: 'red_bg',
					即将我方保养: 'yellw_bg'
				};
				if (!colorOptions[status]) {
					colorOptions[status] = 'yellw_bg';
				}
				return `<div class="marker-content_box ${colorOptions[status]}">${number}</div>`;
			}
		},
		//点击当前标识点弹出框
		popupClick(val) {
			let params = {
				location: val[4] ? val[4] : this.currentLocation
			};
			this.$http.getElevators(params).then(res => {
				res.data.val.forEach(v => {
					return (v.elevatorsName = `${v.id}-${v.type}-期限${v.service_life ? v.service_life : 0}年-${v.maintaining_type}-${v.maintaining_state}`);
				});
				this.elevatorsColums = res.data.val;
				this.currentLocation = val[4];
				this.showPicker = true;
			});
		},
		cancelChange() {
			this.elevatorsColums = this.$options.data.elevatorsColums;
			this.showPicker = false;
		},
		//确认事件
		elevatorsClick(val) {
			Object.assign(val, { location: this.currentLocation });
			this.formData = val;
			this.editVisible = true;
			this.showPicker = false;
		},
		//表单修改回调事件
		editFormChange(val) {
			this.getLocalStorage();
			this.editVisible = false;
			this.popupClick(val);
		}
	}
};
</script>
<style scoped="scoped" lang="less">
/deep/.map-box {
	height: calc(100% - 55px);
	.van-picker-column__item {
		justify-content: left;
		padding: 0 12px;
	}
	.marker-content_box {
		width: 25px;
		height: 25px;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
		box-sizing: border-box;
		font-size: 12px;
		background-color: yellow;
	}
	.red_bg {
		color: #fff;
		background-color: red;
	}
	.yellow_bg {
		background-color: yellow;
	}
	.blue_bg {
		color: #fff;
		background-color: blue;
	}
	.popup-content_box {
		padding: 10px;
		box-sizing: border-box;
		height: 100%;
	}
	.popup-content_title {
		font-weight: bold;
		padding: 0 10px;
	}
	.list-item_content {
		padding: 10px 0;
		box-sizing: border-box;
		border-bottom: 1px solid #ebedf0;
		-webkit-transform: scaleY(0.5);
		transform: scaleY(0.5);
	}
	.van-picker__title {
		font-size: 14px;
		max-width: 65%;
		line-height: inherit;
	}
	.van-picker-column {
		font-size: 14px;
	}
	.van-picker-column__item {
		.van-ellipsis {
			overflow: inherit !important;
			white-space: initial !important;
		}
	}
}
.loading-box {
	position: fixed;
	z-index: 100000;
	width: 100%;
	height: 100%;
	background-color: #fff;
	display: flex;
	align-items: center;
	justify-content: center;
}
.toolbar {
	position: fixed;
	z-index: 100000;
	width: 100%;
	height: 100%;
	background-color: rgba(0, 0, 0, 0.5);
	display: flex;
	align-items: center;
	justify-content: center;
	color: #fff;
}
</style>
