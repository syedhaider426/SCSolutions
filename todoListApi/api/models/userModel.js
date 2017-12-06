'use strict';

var mongoose = require('mongoose'),
bcryptjs = require('bcryptjs'),
Schema = mongoose.Schema;

/**
* User Schema
*/
var UserSchema = new Schema({
	fullName: {
		type: String,
		trim: true,
		required: true
	},
	email: {
		type: String,
		unique: true,
		lowercase: true,
		trim: true,
		required: true
	},
	hash_password: {
		type: String,
		required: true
	},
	created: {
		type: Date,
		default: Date.now
	}
});

UserSchema.methods.comparePassword = function(password)
{
	return bcryptjs.compareSync(password,this.hash_password);
};

mongoose.model('User',UserSchema);
