<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProductController;
use App\Http\Controllers\Category\CategoryController;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');


// Route to store product
Route::post('products', [ProductController::class, 'store']);

// Route to get/show all producct
Route::get('products', [ProductController::class, 'show']);

// get a Product using it slug
Route::get('product/{slug}', [ProductController::class, 'a_product']);

// update a product
Route::put('updateProduct/{slug}', [ProductController::class, 'update']);


Route::group(['prefix' => 'v1'], function() {
    Route::apiResource('categories', CategoryController::class);
});