<?php

namespace App\Http\Controllers\Product;

use App\Models\Product;
use App\Models\SavedProduct;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use App\Http\Resources\SavedProductResource;
use App\Http\Requests\StoreSavedProductRequest;

class SavedProductController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $savedProducts = SavedProduct::all();

        return $this->success('Saved Products Successfully Retrieved', SavedProductResource::collection($savedProducts));
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreSavedProductRequest $request, $user_id, Product $product)
    {
        $validated = $request->validated();

        $validated['user_id'] = $user_id;

        $savedProduct = $product->savedProducts()->create($validated);

        return $this->success('Product Saved Successfully', new SavedProductResource($savedProduct), 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(SavedProduct $savedProduct)
    {
        return $this->success('Saved Product Retrieved Successfully', new SavedProductResource($savedProduct));
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(StoreSavedProductRequest $request, SavedProduct $savedProduct)
    {
        $savedProduct->update($request->validated());

        return $this->success('Saved Product Updated Successfully', new SavedProductResource($savedProduct)); 
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(SavedProduct $savedProduct)
    {
        $savedProduct->delete();

        return response()->noContent();
    }
}
