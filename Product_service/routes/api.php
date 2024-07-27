<?php

use App\Http\Controllers\ProductController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

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



