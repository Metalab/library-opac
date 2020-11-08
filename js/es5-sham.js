/*!
 * https://github.com/es-shims/es5-shim
 * @license es5-shim Copyright 2009-2020 by contributors, MIT License
 * see https://github.com/es-shims/es5-shim/blob/master/LICENSE
 */
!function(e,t){"use strict";"function"==typeof define&&define.amd?define(t):"object"==typeof exports?module.exports=t():e.returnExports=t()}(this,(function(){var e,t,r,n,o=Function.call,c=Object.prototype,i=o.bind(c.hasOwnProperty),f=o.bind(c.propertyIsEnumerable),u=o.bind(c.toString),l=i(c,"__defineGetter__");l&&(e=o.bind(c.__defineGetter__),t=o.bind(c.__defineSetter__),r=o.bind(c.__lookupGetter__),n=o.bind(c.__lookupSetter__));var b=function(e){return null==e||"object"!=typeof e&&"function"!=typeof e};if(Object.getPrototypeOf||(Object.getPrototypeOf=function(e){var t=e.__proto__;return t||null===t?t:"[object Function]"===u(e.constructor)?e.constructor.prototype:e instanceof Object?c:null}),Object.defineProperty){var p=function(e){try{return e.sentinel=0,0===Object.getOwnPropertyDescriptor(e,"sentinel").value}catch(e){return!1}},a=p({});if(!("undefined"==typeof document||p(document.createElement("div")))||!a)var O=Object.getOwnPropertyDescriptor}if(!Object.getOwnPropertyDescriptor||O){Object.getOwnPropertyDescriptor=function(e,t){if(b(e))throw new TypeError("Object.getOwnPropertyDescriptor called on a non-object: "+e);if(O)try{return O.call(Object,e,t)}catch(e){}var o;if(!i(e,t))return o;if(o={enumerable:f(e,t),configurable:!0},l){var u=e.__proto__,p=e!==c;p&&(e.__proto__=c);var a=r(e,t),s=n(e,t);if(p&&(e.__proto__=u),a||s)return a&&(o.get=a),s&&(o.set=s),o}return o.value=e[t],o.writable=!0,o}}if(Object.getOwnPropertyNames||(Object.getOwnPropertyNames=function(e){return Object.keys(e)}),!Object.create){var s;s=!({__proto__:null}instanceof Object)||"undefined"==typeof document?function(){return{__proto__:null}}:function(){var e=function(){if(!document.domain)return!1;try{return!!new ActiveXObject("htmlfile")}catch(e){return!1}}()?function(){var e,t;return(t=new ActiveXObject("htmlfile")).write("<script><\/script>"),t.close(),e=t.parentWindow.Object.prototype,t=null,e}():function(){var e,t=document.createElement("iframe"),r=document.body||document.documentElement;return t.style.display="none",r.appendChild(t),t.src="javascript:",e=t.contentWindow.Object.prototype,r.removeChild(t),t=null,e}();delete e.constructor,delete e.hasOwnProperty,delete e.propertyIsEnumerable,delete e.isPrototypeOf,delete e.toLocaleString,delete e.toString,delete e.valueOf;var t=function(){};return t.prototype=e,s=function(){return new t},new t},Object.create=function(e,t){var r,n=function(){};if(null===e)r=s();else{if(b(e))throw new TypeError("Object prototype may only be an Object or null");n.prototype=e,(r=new n).__proto__=e}return void 0!==t&&Object.defineProperties(r,t),r}}var j,d=function(e){try{return Object.defineProperty(e,"sentinel",{}),"sentinel"in e}catch(e){return!1}};if(Object.defineProperty){var y=d({}),_="undefined"==typeof document||d(document.createElement("div"));if(!y||!_)var w=Object.defineProperty,v=Object.defineProperties}if(!Object.defineProperty||w){Object.defineProperty=function(o,i,f){if(b(o))throw new TypeError("Object.defineProperty called on non-object: "+o);if(b(f))throw new TypeError("Property description must be an object: "+f);if(w)try{return w.call(Object,o,i,f)}catch(e){}if("value"in f)if(l&&(r(o,i)||n(o,i))){var u=o.__proto__;o.__proto__=c,delete o[i],o[i]=f.value,o.__proto__=u}else o[i]=f.value;else{var p="get"in f,a="set"in f;if(!l&&(p||a))throw new TypeError("getters & setters can not be defined on this javascript engine");p&&e(o,i,f.get),a&&t(o,i,f.set)}return o}}Object.defineProperties&&!v||(Object.defineProperties=function(e,t){if(v)try{return v.call(Object,e,t)}catch(e){}return Object.keys(t).forEach((function(r){"__proto__"!==r&&Object.defineProperty(e,r,t[r])})),e}),Object.seal||(Object.seal=function(e){if(Object(e)!==e)throw new TypeError("Object.seal can only be called on Objects.");return e}),Object.freeze||(Object.freeze=function(e){if(Object(e)!==e)throw new TypeError("Object.freeze can only be called on Objects.");return e});try{Object.freeze((function(){}))}catch(e){Object.freeze=(j=Object.freeze,function(e){return"function"==typeof e?e:j(e)})}Object.preventExtensions||(Object.preventExtensions=function(e){if(Object(e)!==e)throw new TypeError("Object.preventExtensions can only be called on Objects.");return e}),Object.isSealed||(Object.isSealed=function(e){if(Object(e)!==e)throw new TypeError("Object.isSealed can only be called on Objects.");return!1}),Object.isFrozen||(Object.isFrozen=function(e){if(Object(e)!==e)throw new TypeError("Object.isFrozen can only be called on Objects.");return!1}),Object.isExtensible||(Object.isExtensible=function(e){if(Object(e)!==e)throw new TypeError("Object.isExtensible can only be called on Objects.");for(var t="";i(e,t);)t+="?";e[t]=!0;var r=i(e,t);return delete e[t],r})}));
//# sourceMappingURL=es5-sham.js.map
