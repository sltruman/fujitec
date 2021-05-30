var tools = {
  //空对象转为空数组
  stringify: function(data) {
    return JSON.stringify(data) == '{}' ? [] : data;
  },
  //两个对象取交集
  objIntersection: function(obj1, obj2) {
    Object.keys(obj2).map(function(key) {
      obj1.hasOwnProperty(key) && (obj2[key] = obj1[key]);
    });
    return obj2;
  }
}
export default tools;
