import Fuse from "https://cdn.jsdelivr.net/npm/fuse.js@6.6.2/dist/fuse.esm.js";
import techniques from "./techniques.js";
export default {
  data() {
    return {
      searchValue: "",
      techlist: techniques,
      partchecked: true,
      typechecked: true,
      noteschecked: true,
      partnamechecked: true,
    };
  },
  watch: {
    searchValue(newValue, _) {
      if (newValue != "" && newValue) {
        this.getResult();
      } else {
        this.techlist = techniques;
      }
    },
  },
  methods: {
    getResult() {
      let options = {
        includeScore: true,
        keys: [],
      };
      if (this.partchecked) {
        options.keys.push("Parts");
      }
      if (this.typechecked) {
        options.keys.push("Type");
      }
      if (this.noteschecked) {
        options.keys.push("Notes");
      }
      if (this.partnamechecked) {
        options.keys.push("Partnames");
      }
      const fuse = new Fuse(techniques, options);
      console.log(this.searchValue);
      const result = fuse.search(this.searchValue);
      console.log("result: ", result);
      this.techlist = result.map((x) => x.item);
    },
    techparts(parts) {
      if (parts != "" && parts) {
        return parts.toString();
      }
      return "";
    },
  },
};
