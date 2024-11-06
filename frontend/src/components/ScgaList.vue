<template>
	<div>
		<p>{{ baseline }}</p>
		<ul>
			<li></li>
		</ul>
	</div>
</template>

<script>
import axios from "axios";
export default {
	name: "ScgaList",

	data() {
		return {
			info: "",
			baseline: "",
			file_name: "",
		};
	},
	mounted() {
		this.getScgaInfo();
	},

	methods: {
		getScgaInfo: function () {
			let url = "/api/scgas";
			axios
				.get(url)
				.then((response) => {
					this.info = response.data;
					console.log(this.info);
					this.baseline = this.info.results[0].baseline;
					this.file_name = this.info.results[0].file_name;
					console.log(this.baseline);
					if (!isNaN(this.info)) {
					}
				})
				.catch((error) => {
					console.log("error", error);
				});
		},
	},
};
</script>
