<?php
/**
 * @license AiFactory
 */
declare(strict_types=1);

namespace App\Form;

use App\Entity\Product;
use App\Form\DataTransformer\BrandToIntTransformer;
use App\Form\DataTransformer\CategoryToIntTransformer;
use App\Form\DataTransformer\PlayerToIntTransformer;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;

/**
 * Class ProductType.
 */
class ProductType extends AbstractType
{
    private BrandToIntTransformer $brandToIntTransformer;

    private CategoryToIntTransformer $categoryToIntTransformer;

    private PlayerToIntTransformer $playerToIntTransformer;

    public function __construct(
        BrandToIntTransformer $brandToIntTransformer,
        CategoryToIntTransformer $categoryToIntTransformer,
        PlayerToIntTransformer $playerToIntTransformer
    ) {
        $this->brandToIntTransformer = $brandToIntTransformer;
        $this->categoryToIntTransformer = $categoryToIntTransformer;
        $this->playerToIntTransformer = $playerToIntTransformer;
    }

    /**
     * @param FormBuilderInterface $builder
     * @param array                $options
     */
    public function buildForm(FormBuilderInterface $builder, array $options)
    {
        $builder
            ->add('clientId', TextType::class)
            ->add('name', TextType::class)
            ->add('tags', TextType::class)
            ->add('brand', IntegerType::class)
            ->add('category', IntegerType::class)
            ->add('player', IntegerType::class);

        $builder->get('brand')->addModelTransformer($this->brandToIntTransformer);
        $builder->get('category')->addModelTransformer($this->categoryToIntTransformer);
        $builder->get('player')->addModelTransformer($this->playerToIntTransformer);
    }

    /**
     * @param OptionsResolver $resolver
     */
    public function configureOptions(OptionsResolver $resolver)
    {
        $resolver->setDefaults(
            [
                'data_class' => Product::class,
                'csrf_protection' => false,
                'allow_extra_fields' => false,
            ]
        );
    }
}
