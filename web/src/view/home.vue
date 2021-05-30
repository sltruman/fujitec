<template>
	<div style="height: 100%;">
		<van-nav-bar title="富士达" :left-arrow="editVisible" @click-left="onClickLeft" />
		<div class="map-box" v-show="!editVisible">
			<el-amap vid="amapDemo" viewMode="3D" :plugin="plugins" :zoom="zoom" :resizeEnable="true" :isHotspot="true">
				<el-amap-marker
					v-for="(item, index) in markerGroups"
					:key="index"
					:position="[item.loinitude, item.latitude]"
					:visible="true"
					:content="getContentHtml(item.elevators)"
					:draggable="false"
					:events="events"
					:extData="item"
				></el-amap-marker>
			</el-amap>
			<!-- 编辑框 -->
			<van-popup v-model="showPicker" :close-on-popstate="true" :overlay="false" position="bottom">
				<van-picker show-toolbar :title="currentLocation" value-key="elevatorsName" :columns="elevatorsColums" @confirm="elevatorsClick" @cancel="cancelChange"></van-picker>
			</van-popup>
		</div>
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
		return {
			// 缩放级别
			zoom: 17,
			//工具插件
			plugins: ['AMap.ToolBar'],
			// 定义点坐标组数组
			markerGroups: [],
			events: {
				click: a => {
					this.$nextTick(() => {
						this.popupClick(a.target.w.extData);
					});
				}
			},
			showPicker: false,
			elevatorsColums: [],
			currentLocation: '',
			formData: {},
			editVisible: false
		};
	},
	created() {
		this.getData();
	},
	methods: {
		onClickLeft() {
			this.editVisible = false;
			this.showPicker = true;
			this.getData();
		},
		getData() {
			this.$http
				.getElevators()
				.then(res => {
					this.markerGroups = res.data.val;
				})
				.catch(e => {
					console.log(e);
				});
		},
		getContentHtml(val) {
			// 未避免被简书转化未设置img的src属性
			let colorOptions = {
				第三方保养: 'blue_bg',
				我方保养: 'red_bg',
				即将我方保养: 'yellw_bg'
			};
			if (!colorOptions[val[0].maintaining_type]) {
				colorOptions[val[0].maintaining_type] = 'yellw_bg';
			}
			return `<div class="marker-content_box ${colorOptions[val[0].maintaining_type]}">${val.length}</div>`;
		},
		popupClick(val) {
			val.elevators.forEach((v, k) => {
				return (v.elevatorsName = `${k + 1}.${v.type}_期限${v.service_life}_${v.maintaining_type}_${v.maintaining_state}`);
			});
			this.elevatorsColums = val.elevators;
			this.currentLocation = val.location;
			this.showPicker = true;
		},
		cancelChange() {
			this.elevatorsColums = this.$options.data.elevatorsColums;
			this.showPicker = false;
		},
		elevatorsClick(val) {
			Object.assign(val, { location: this.currentLocation });
			this.formData = val;
			this.editVisible = true;
			this.showPicker = false;
		},
		editFormChange() {
			this.editVisible = false;
			this.showPicker = true;
			this.getData();
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
	.van-picker__title{
		font-size: 14px;
		max-width: 80%;
		line-height: inherit;
	}
	.van-picker-column{
		font-size: 14px;
	}
}

</style>
