<?php

namespace App\Http\Controllers;

use App\Http\Requests\Product\CreateProductRequest;
use App\Models\Product;
use Illuminate\Http\Request;
use Illuminate\Validation\ValidationException;
use Illuminate\Support\Facades\Log;


class ProductController extends Controller
{


    public function store(CreateProductRequest $request)
    {
        try {
            // Search if name exists
            $name = $request->name;

            $count = 2;
            while (Product::where('name', $name)->exists()) {
                $name = $request->name . ' ' . $count;
                $count++;
            }

            // Store product model in a variable
            $product = new Product();

            // Convert string to slug

            $slug = strtolower(trim(preg_replace('/[\s-]+/', '-', preg_replace('/[^A-Za-z0-9-]+/', '-', preg_replace('/[&]/', 'and', preg_replace('/[\']/', '', iconv('UTF-8', 'ASCII//TRANSLIT', $name))))), '-'));
            
            // Collect user info and store in the appropriate column
            $product->name = $name;
            $product->category_id = $request->category_id;
            $product->slug = $slug;
            $product->price = $request->price;
            $product->description = $request->description;
            $product->is_visible = $request->is_visible;
            $product->is_approved = $request->is_approved;

            // Save product details
            $result = $product->save();

            // Check if it submitted successfully
            if ($result) {
                return response()->json([
                    'Status' => 'success',
                    'Message' => 'Product created successfully',
                    'Data' => [
                        'id' => $product->id,
                        'name' => $product->name,
                        'slug' => $product->slug,
                        // Add other necessary fields here
                    ]
                ], 201);
            } else {
                return response()->json(['message' => 'Oops! Something went wrong'], 500);
            }
        } catch (ValidationException $e) {
            // Log validation errors
            Log::error(json_encode($e->errors()));
            return response()->json(['errors' => $e->errors()], 422);
        } catch (\Exception $e) {
            // Log general errors
            Log::error($e->getMessage());
            return response()->json(['message' => 'An unexpected error occurred. Please try again later.'], 500);
        }
    }

    public function show()
    {
        $products = Product::paginate(10); // Retrieves 10 products per page
    
        return response()->json([
            'Status' => 'success',
            'Message' => 'Products retrieved successfully',
            'Data' => $products->map(function($product) {
                return [
                    'id' => $product->id,
                    'name' => $product->name,
                    'slug' => $product->slug,
                    // Add other necessary fields here
                ];
            }),
            'Pagination' => [
                'total' => $products->total(),
                'per_page' => $products->perPage(),
                'current_page' => $products->currentPage(),
                'last_page' => $products->lastPage(),
                'from' => $products->firstItem(),
                'to' => $products->lastItem()
            ]
        ], 200);

        
    }
    

    public function a_product($slug)
    {

       $product = Product::where('slug', $slug)->first();

       return response()->json([
        'Status' => 'success',
        'Message' => "{$product->name} Received retrieved successfully",
        'Data' => [
                       
                'name' => $product->name,
        ],
        
        
    ], 200);

    }

    public function update(Request $request, $slug)
{
    try {
        // Find the product by slug
        $product = Product::where('slug', '=', $slug)->first();
       
        // Update the product details
        $product->name = $request->name;
        $product->category_id = $request->category_id;
        $product->slug = $request->slug;
        $product->price = $request->price;
        $product->description = $request->description;
        $product->is_visible = $request->is_visible;
        $product->is_approved = $request->is_approved;

        // Save the updated product
        $updated = $product->save();

        if ($updated) {
            return response()->json([
                'Status' => 'success',
                'Message' => 'Product updated successfully',
                'Data' => [
                    'id' => $product->id,
                    'name' => $product->name,
                    'slug' => $product->slug,
                    // Add other necessary fields here
                ]
            ], 200);
        } else {
            return response()->json(['message' => 'Oops! Something went wrong'], 500);
        }
    } catch (ValidationException $e) {
        // Log validation errors
        Log::error(json_encode($e->errors()));
        return response()->json(['errors' => $e->errors()], 422);
    } catch (\Exception $e) {
        // Handle other errors
        Log::error($e->getMessage());
        return response()->json(['message' => 'An unexpected error occurred. Please try again later.'], 500);
    }
}

public function delete($id){

        $delete = Product::where('id', $id);

        if ($delete) {
            $delete->delete();
        }
}

}
