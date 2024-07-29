<?php

namespace App\Http\Controllers\Product;

use App\Models\SavedProduct;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use App\Http\Resources\SavedProductResource;

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
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        //
    }
}
