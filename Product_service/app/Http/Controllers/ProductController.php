<?php

namespace App\Http\Controllers;

use App\Models\Product;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Tymon\JWTAuth\Facades\JWTAuth;

class ProductController extends Controller
{

    // public function __construct()
    // {
    //     $this->middleware('auth:api', ['except' => ['login']]);
    // }
    //  create / add product
    public function add_new_product(Request $request)
    {
        try {
         // validate data from users
        $validated = $request->validate([
            'name' => 'required|max:255',
            'category_id' => 'required',
            'slug' => 'string|max:255',
            'price' => 'integer',
            'description' => 'string|max:255',
            'is_visible' => 'boolean',
            'is_approved' => 'boolean'
        ]);

    } catch (ValidationException $e) {
        // Log validation e rrors
        \Log::error($e->errors());
        return response()->json(['errors' => $e->errors()], 422);
    }

        // search if name exist
        $name = $request->name;
        $count = 2;
        while (Product::where('name', $name)->exists()) {
            $name = $request->name . ' ' . $count;
            $count++;
            
            
        }
        
        // store product model in a variable
        $product = New Product();
       
        // Collect user info and store in a the appropriate column
        $product->name =  $name;
        $product->category_id = $request->category_id;
        $product->slug = $request->slug;
        $product->price = $request->price;
        $product->description = $request->description;
        $product->is_visible = $request->is_visible;
        $product->is_approved = $request->is_approved;

        // now create a variable to hold save product details
        $result = $product->save();
        //check if it submitted successfully
        if ($result) {  
            return response()->json(['message' => 'Product added successfully'], 201);
        }
        else
        {
            return response()->json(['message' => 'Opps! Something went wrong'], 419);
        }


    }

    
}
