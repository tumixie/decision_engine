/**
 * Created by tumixie on 2018/8/13.
 */

// function $(Nid){
//  return document.getElementById(Nid);
// }

function openDialogView(title,url,width,height){

    if(navigator.userAgent.match(/(iPhone|iPod|Android|ios)/i)){//如果是移动端，就使用自适应大小弹窗
		width='auto';
		height='auto';
	}else{//如果是PC端，根据用户设置的width和height显示。

	}
	top.layer.open({
	    type: 2,
	    area: [width, height],
	    title: title,
        maxmin: true, //开启最大化最小化按钮
	    content: url ,
	    shadeClose: true,
	    btn: ['关闭'],
	    cancel: function(index){
	       }
	});

}

function search(){//查询，页码清零
	$("#lookForCondition").submit();
		return false;
}
