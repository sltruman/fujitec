<template>
	<div class="list-item_box">
		<div class="list-item_title">{{ form.location }}</div>
		<van-form>
			<van-field name="stepper" label="使用期限">
				<template #input>
					<van-stepper v-model="form.service_life" :min="0" :max="100" integer />
				</template>
			</van-field>
			<van-field readonly clickable name="picker" label="保养类型" :value="form.type" placeholder="请选择" @click="typePicker = true" />
			<van-popup v-model="typePicker" position="bottom">
				<van-picker show-toolbar :default-index="form.type" :columns="typeColumns" @confirm="typeConfirm" @cancel="typePicker = false" />
			</van-popup>
			<van-field readonly clickable name="picker" label="维护方" :value="form.maintaining_type" placeholder="请选择" @click="maintainTypePicker = true" />
			<van-popup v-model="maintainTypePicker" position="bottom">
				<van-picker show-toolbar :columns="maintainTypeColums" :default-index="form.maintaining_type" @confirm="maintainConfirm" @cancel="maintainTypePicker = false" />
			</van-popup>
			<div style="margin: 16px;"><van-button block type="info" @click="submitOk">保存</van-button></div>
		</van-form>
	</div>
</template>

<script>
export default {
	name: 'editForm',
	props: {
		formData: {
			type: null
		}
	},
	watch: {
		formData(newV) {
			this.formData = newV;
			this.form = this.$tools.objIntersection(this.formData, this.form);
		}
	},
	data() {
		return {
			form: {
				location: '',
				id: '',
				service_life: '',
				type: '',
				maintaining_type: ''
			},
			typeColumns: ['升降梯', '扶梯'],
			typePicker: false,
			maintainTypePicker: false,
			maintainTypeColums: ['我方保养', '代理商保养', '即将我方保养', '第三方保养'],
			editVisible: false
		};
	},
	created() {
		this.form = this.$tools.objIntersection(this.formData, this.form);
	},
	methods: {
		typeConfirm(val) {
			this.form.type = val;
			this.typePicker = false;
		},
		maintainConfirm(val) {
			this.form.maintaining_type = val;
			this.maintainTypePicker = false;
		},
		submitOk() {
			let params = this.form;
			this.$http
				.setElevators(params)
				.then(() => {
					this.$emit('change', params);
				})
				.catch(() => {
					this.$emit('change', params);
				});
		}
	}
};
</script>

<style scoped="scoped">
.list-item_box {
	background-color: #fff;
}
.list-item_title {
	box-sizing: border-box;
	padding: 10px;
}
</style>
