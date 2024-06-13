# Difference between var, let and const

* variables created by using var and let can be reintialize.
* variables created by const cannot be reintialize.

* varaibles created by var has function or global scope.
* variables created by const or let has block scope.

* variables created by var is hoisted and intialized as undefined.
* variables created by let is hoisted but not intialized, so using that will raise a  ReferenceError.

* variables created by var can be redeclared.
* variables created by let cannot.

* var should only be used if you want to support older browser.