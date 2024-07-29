<?php

namespace App\Http\Controllers\Category;

use App\Models\Category;
use Illuminate\Support\Str;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use App\Http\Requests\StoreCategoryRequest;

class CategoryController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $categories = Category::all();

        return $this->success('Categories Successful', $categories);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreCategoryRequest $request)
    {
        $validated = $request->validated();

        $validated['slug'] = Str::slug($validated['name']);

        $category = Category::create($validated);

        return $this->success('Categories created successfully', $category, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Category $category)
    {
        return $this->success('Category Retrieved Successfully.', $category);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(StoreCategoryRequest $request, Category $category)
    {
        $category->update($request->validated());

        return $this->success('Category successfully updated.', $category);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Category $category)
    {
        $category->delete();

        return response()->noContent();
    }
}
